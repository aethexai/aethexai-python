"""WebRTC Conversation with an Aethex agent.

Requires: pip install aethexai[realtime]
"""

from __future__ import annotations

import asyncio
import fractions
import json
import logging
import struct
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aethexai.client import AsyncAethexAI

logger = logging.getLogger(__name__)

RATE = 48_000
FRAME_SAMPLES = 960


def _stereo_to_mono(data: bytes) -> bytes:
    """Convert interleaved stereo s16 PCM to mono by averaging channels."""
    samples = struct.unpack(f"<{len(data) // 2}h", data)
    mono = []
    for i in range(0, len(samples), 2):
        mono.append((samples[i] + samples[i + 1]) // 2)
    return struct.pack(f"<{len(mono)}h", *mono)


@dataclass
class ConversationCallbacks:
    """Callbacks fired during a WebRTC conversation."""

    on_agent_audio: Callable[[bytes], Any] | None = None
    on_agent_text: Callable[[str], Any] | None = None
    on_user_transcript: Callable[[str], Any] | None = None
    on_metrics: Callable[[dict], Any] | None = None
    on_status_change: Callable[[str], Any] | None = None
    on_error: Callable[[Exception], Any] | None = None


class SilenceTrack:
    """A MediaStreamTrack that produces 20ms frames of silence at 48kHz.

    Used when no audio_input is provided (e.g. text-only interaction or
    when the caller feeds audio via a separate mechanism).
    """

    kind = "audio"

    def __init__(self) -> None:
        try:
            import av
            from aiortc.mediastreams import MediaStreamTrack
        except ImportError:
            raise ImportError(
                "aiortc and av are required for WebRTC. "
                "Install with: pip install aethexai[realtime]"
            )
        self._track = _make_silence_track()


def _make_silence_track():  # type: ignore[no-untyped-def]
    """Create a MediaStreamTrack subclass that emits silence frames."""
    import av
    from aiortc.mediastreams import MediaStreamTrack

    class _SilenceTrackImpl(MediaStreamTrack):
        kind = "audio"

        def __init__(self) -> None:
            super().__init__()
            self._pts = 0
            self._silence = b"\x00" * (FRAME_SAMPLES * 2)

        async def recv(self):  # type: ignore[no-untyped-def]
            await asyncio.sleep(0.02)
            frame = av.AudioFrame(format="s16", layout="mono", samples=FRAME_SAMPLES)
            frame.planes[0].update(self._silence)
            frame.sample_rate = RATE
            frame.pts = self._pts
            frame.time_base = fractions.Fraction(1, RATE)
            self._pts += FRAME_SAMPLES
            return frame

    return _SilenceTrackImpl()


class Conversation:
    """High-level WebRTC conversation with an Aethex agent.

    Requires: ``pip install aethexai[realtime]``

    Usage::

        from aethexai import AsyncAethexAI
        from aethexai.realtime import Conversation, ConversationCallbacks

        client = AsyncAethexAI(api_key="ak_live_...")
        conv = Conversation(
            client, agent_id="ag_...",
            callbacks=ConversationCallbacks(
                on_agent_audio=lambda data: play(data),
                on_agent_text=lambda text: print(text),
            ),
        )
        await conv.start()
        # ... conversation runs ...
        await conv.end()
    """

    def __init__(
        self,
        client: AsyncAethexAI,
        agent_id: str,
        *,
        callbacks: ConversationCallbacks | None = None,
        audio_input: Any | None = None,
        mono_audio: bool = True,
    ) -> None:
        self._client = client
        self._agent_id = agent_id
        self._callbacks = callbacks or ConversationCallbacks()
        self._audio_input = audio_input
        self._mono_audio = mono_audio

        self._pc: Any = None
        self._dc: Any = None
        self._session_id: str = ""
        self._capture_task: asyncio.Task | None = None  # type: ignore[type-arg]
        self._ping_task: asyncio.Task | None = None  # type: ignore[type-arg]
        self._connected = False

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def is_connected(self) -> bool:
        return self._connected

    async def start(self) -> None:
        """Establish the WebRTC connection to the agent."""
        from aethexai.realtime._aioice_patches import apply_patches

        apply_patches()

        from aiortc import (
            RTCConfiguration,
            RTCIceServer,
            RTCPeerConnection,
            RTCSessionDescription,
        )

        session_data = await self._client.conversation_connect(agent_id=str(self._agent_id))
        self._session_id = session_data["session_id"]
        logger.info("Session %s created", self._session_id[:8])
        self._notify_status("connecting")

        ice_servers: list[Any] = []
        for s in session_data.get("ice_config", {}).get("iceServers", []):
            urls = s.get("urls", [])
            if isinstance(urls, str):
                urls = [urls]
            ice_servers.append(
                RTCIceServer(
                    urls=urls,
                    username=s.get("username"),
                    credential=s.get("credential"),
                )
            )
        if not ice_servers:
            ice_servers = [RTCIceServer(urls=["stun:stun.l.google.com:19302"])]
        logger.info("ICE servers: %s", [s.urls for s in ice_servers])

        pc = RTCPeerConnection(configuration=RTCConfiguration(iceServers=ice_servers))
        self._pc = pc

        audio_track = self._audio_input or _make_silence_track()
        pc.addTransceiver(audio_track, direction="sendrecv")
        pc.addTransceiver("video", direction="recvonly")
        pc.addTransceiver("video", direction="recvonly")

        dc = pc.createDataChannel("chat", ordered=True)
        self._dc = dc
        dc_open = asyncio.Event()

        def on_dc_open() -> None:
            logger.info("Data channel open for session %s", self._session_id[:8])
            for idx, enabled in [(0, True), (1, False), (2, False)]:
                dc.send(
                    json.dumps(
                        {
                            "type": "signalling",
                            "message": {
                                "type": "trackStatus",
                                "receiver_index": idx,
                                "enabled": enabled,
                            },
                        }
                    )
                )
            self._ping_task = asyncio.ensure_future(self._ping_loop())
            dc_open.set()

        dc.on("open", on_dc_open)

        @dc.on("message")
        def on_dc_message(message: str | bytes) -> None:
            if isinstance(message, bytes):
                return
            try:
                msg = json.loads(message)
            except (json.JSONDecodeError, TypeError):
                return
            msg_type = msg.get("type", "")
            if msg_type == "agent_text" and self._callbacks.on_agent_text:
                self._callbacks.on_agent_text(msg.get("text", ""))
            elif msg_type == "user_transcript" and self._callbacks.on_user_transcript:
                self._callbacks.on_user_transcript(msg.get("text", ""))
            elif msg_type == "metrics" and self._callbacks.on_metrics:
                self._callbacks.on_metrics(msg)

        @pc.on("track")
        def on_track(track: Any) -> None:
            logger.info("Track received: kind=%s", track.kind)
            if track.kind == "audio":
                self._capture_task = asyncio.ensure_future(self._capture_audio(track))

        @pc.on("connectionstatechange")
        def on_conn_state() -> None:
            state = pc.connectionState
            logger.info("Connection state: %s", state)
            self._notify_status(state)
            if state in ("failed", "closed"):
                self._connected = False

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        deadline = asyncio.get_event_loop().time() + 30
        while pc.iceGatheringState != "complete":
            if asyncio.get_event_loop().time() > deadline:
                logger.warning("ICE gathering timeout, proceeding with partial candidates")
                break
            await asyncio.sleep(0.2)
        logger.info("ICE gathering done (state=%s)", pc.iceGatheringState)

        sdp = pc.localDescription.sdp
        answer = await self._client.send_offer(
            self._session_id,
            sdp=sdp,
            type=pc.localDescription.type,
        )
        logger.info("SDP answer received")

        await pc.setRemoteDescription(RTCSessionDescription(sdp=answer["sdp"], type=answer["type"]))

        connected = False
        for _ in range(200):
            await asyncio.sleep(0.1)
            if dc_open.is_set():
                connected = True
                break
            if pc.connectionState == "connected":
                try:
                    await asyncio.wait_for(dc_open.wait(), 3)
                    connected = True
                except asyncio.TimeoutError:
                    logger.warning("Data channel didn't open, proceeding anyway")
                    connected = True
                break
            if pc.connectionState in ("failed", "closed"):
                err = RuntimeError(
                    f"WebRTC connection {pc.connectionState} (iceState={pc.iceConnectionState})"
                )
                self._notify_error(err)
                raise err

        if not connected:
            err = RuntimeError(
                f"WebRTC connection timeout "
                f"(connState={pc.connectionState}, "
                f"iceState={pc.iceConnectionState})"
            )
            self._notify_error(err)
            raise err

        self._connected = True
        self._notify_status("connected")
        logger.info("Session %s connected", self._session_id[:8])

    async def end(self) -> None:
        """End the conversation and close the WebRTC connection."""
        if self._ping_task and not self._ping_task.done():
            self._ping_task.cancel()
        if self._capture_task and not self._capture_task.done():
            self._capture_task.cancel()

        if self._session_id:
            try:
                await self._client.end_conversation_session(self._session_id)
            except Exception as exc:
                logger.debug("Error ending session: %s", exc)

        if self._pc:
            await self._pc.close()
            self._pc = None

        self._connected = False
        self._notify_status("closed")

    async def _capture_audio(self, track: Any) -> None:
        """Receive audio frames from the remote track and invoke callback."""
        try:
            import av
        except ImportError:
            return

        resampler = av.AudioResampler(format="s16", layout="mono")
        count = 0
        while True:
            try:
                frame = await asyncio.wait_for(track.recv(), 15.0)
                if frame is None:
                    continue
                out_frames = resampler.resample(frame)
                pcm = b""
                for f in out_frames:
                    pcm += bytes(f.planes[0])
                if self._mono_audio:
                    if frame.layout.name != "mono" and len(pcm) >= 4:
                        pcm = _stereo_to_mono(pcm)
                if pcm and self._callbacks.on_agent_audio:
                    self._callbacks.on_agent_audio(pcm)
                count += 1
            except asyncio.TimeoutError:
                logger.warning("Audio capture: 15s timeout waiting for frame")
                break
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.debug("Audio capture ended: %s", exc)
                break
        logger.info("Audio capture stopped after %d frames", count)

    async def _ping_loop(self) -> None:
        """Send periodic pings over the data channel to keep it alive."""
        import time as _time

        while True:
            try:
                if self._dc and self._dc.readyState == "open":
                    self._dc.send("ping: " + str(_time.monotonic()))
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                break
            except Exception:
                break

    def _notify_status(self, status: str) -> None:
        if self._callbacks.on_status_change:
            try:
                self._callbacks.on_status_change(status)
            except Exception:
                pass

    def _notify_error(self, exc: Exception) -> None:
        if self._callbacks.on_error:
            try:
                self._callbacks.on_error(exc)
            except Exception:
                pass
