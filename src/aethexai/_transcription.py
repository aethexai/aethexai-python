"""Client-side WAV chunking helpers shared by the transcription wrappers."""

from __future__ import annotations

import math
import wave
from array import array
from io import BytesIO
from typing import Any, BinaryIO

from aethexai._exceptions import ValidationError
from aethexai._generated.models.body_transcribe_async_api_v1_transcribe_async_post import (
    BodyTranscribeAsyncApiV1TranscribeAsyncPost,
)
from aethexai._generated.models.body_transcribe_sync_api_v1_transcribe_post import (
    BodyTranscribeSyncApiV1TranscribePost,
)
from aethexai._generated.types import File

try:
    import av as _av

    av: Any = _av
except ImportError:
    av = None

CHUNK_SECONDS = 30
MAX_REQUEST_SECONDS = 35
WINDOW_MS = 50
CANONICAL_RATE = 24000
CANONICAL_CHANNELS = 1
CANONICAL_SAMPWIDTH = 2


def to_canonical_wav(data: bytes) -> bytes | None:
    """Transcode any audio bytes to 24000 Hz mono 16-bit PCM WAV via PyAV, or None."""
    if av is None:
        return None
    try:
        resampler = av.AudioResampler(format="s16", layout="mono", rate=CANONICAL_RATE)
        out = BytesIO()
        with av.open(BytesIO(data)) as container:
            stream = next(s for s in container.streams if s.type == "audio")
            with av.open(out, mode="w", format="wav") as output:
                out_stream = output.add_stream("pcm_s16le", rate=CANONICAL_RATE)
                out_stream.layout = "mono"
                for frame in container.decode(stream):
                    frame.pts = None
                    for resampled in resampler.resample(frame):
                        for packet in out_stream.encode(resampled):
                            output.mux(packet)
                for resampled in resampler.resample(None):
                    for packet in out_stream.encode(resampled):
                        output.mux(packet)
                for packet in out_stream.encode(None):
                    output.mux(packet)
        return out.getvalue() or None
    except Exception:
        return None


def prepare_wav(data: bytes) -> bytes | None:
    """Normalize to canonical 24000 Hz mono 16-bit WAV via PyAV; without PyAV pass native-rate mono 16-bit WAV through; else None."""
    try:
        with wave.open(BytesIO(data)) as wav:
            mono_pcm16 = (
                wav.getnchannels() == CANONICAL_CHANNELS
                and wav.getsampwidth() == CANONICAL_SAMPWIDTH
            )
            if mono_pcm16 and (av is None or wav.getframerate() == CANONICAL_RATE):
                return data
    except (wave.Error, EOFError):
        pass
    if av is None:
        return None
    return to_canonical_wav(data)


def _emit_wav(nchannels: int, sampwidth: int, framerate: int, frames: bytes) -> bytes:
    """Wrap raw PCM frames in a WAV container."""
    buffer = BytesIO()
    with wave.open(buffer, "wb") as out:
        out.setnchannels(nchannels)
        out.setsampwidth(sampwidth)
        out.setframerate(framerate)
        out.writeframes(frames)
    return buffer.getvalue()


def silence_split(
    wav_bytes: bytes, chunk_seconds: int = CHUNK_SECONDS, *, search_band_seconds: float = 2.0
) -> list[bytes] | None:
    """Split canonical mono 16-bit WAV into <=chunk_seconds chunks cutting at lowest-RMS seams, else None."""
    try:
        with wave.open(BytesIO(wav_bytes)) as wav:
            nchannels, sampwidth = wav.getnchannels(), wav.getsampwidth()
            framerate, total = wav.getframerate(), wav.getnframes()
            if framerate <= 0 or sampwidth != 2 or nchannels != 1:
                return None
            step = framerate * chunk_seconds
            if step <= 0 or total <= step:
                return None
            samples = array("h")
            samples.frombytes(wav.readframes(total))
    except (wave.Error, EOFError):
        return None
    band = max(1, int(framerate * search_band_seconds))
    window = max(1, int(framerate * WINDOW_MS / 1000))
    chunks = []
    start = 0
    while total - start > step:
        target = start + step
        lo = max(start + window, target - band)
        cut = target
        best = None
        pos = lo
        while pos < target:
            seg = samples[pos : pos + window]
            rms = math.sqrt(sum(s * s for s in seg) / len(seg)) if seg else 0.0
            if best is None or rms <= best:
                best, cut = rms, pos
            pos += window
        chunks.append(_emit_wav(nchannels, sampwidth, framerate, samples[start:cut].tobytes()))
        start = cut
    if start < total:
        chunks.append(_emit_wav(nchannels, sampwidth, framerate, samples[start:total].tobytes()))
    return chunks


def prepare_chunks(data: bytes, chunk_seconds: int = CHUNK_SECONDS) -> list[bytes] | None:
    """Normalize ``data`` to canonical WAV and return the chunks to send, or ``None`` to send raw."""
    prepared = prepare_wav(data)
    if prepared is None:
        return None
    return silence_split(prepared, chunk_seconds) or [prepared]


def merge_transcriptions(results: list[Any]) -> Any:
    """Merge per-chunk transcription responses into the first (space-joined text, summed duration)."""
    merged = results[0]
    texts = [(r.text or "").strip() for r in results if (r.text or "").strip()]
    merged.text = " ".join(texts)
    durations = [
        r.duration_seconds for r in results if isinstance(r.duration_seconds, (int, float))
    ]
    if durations:
        merged.duration_seconds = sum(durations)
    return merged


def build_sync_body(
    data: bytes,
    *,
    file_name: str | None,
    mime_type: str | None,
    language: Any,
) -> BodyTranscribeSyncApiV1TranscribePost:
    """Build a sync-transcribe ``Body`` from already-read ``data`` bytes."""
    return BodyTranscribeSyncApiV1TranscribePost(
        file=File(payload=BytesIO(data), file_name=file_name, mime_type=mime_type),
        language=language,
    )


def guard_async_body(
    body: BodyTranscribeAsyncApiV1TranscribeAsyncPost,
) -> BodyTranscribeAsyncApiV1TranscribeAsyncPost:
    """Guard a >35s WAV, then rebuild the async ``body`` from the read bytes (never the consumed stream)."""
    data = coerce_to_bytes(getattr(body, "file", None))
    if data is None:
        return body
    guard_request_length(data)
    return BodyTranscribeAsyncApiV1TranscribeAsyncPost(
        file=File(
            payload=BytesIO(data), file_name=body.file.file_name, mime_type=body.file.mime_type
        ),
        language=body.language,
        webhook_url=body.webhook_url,
    )


def wav_seconds(data: bytes) -> float | None:
    """Return WAV duration in seconds, or ``None`` if not a valid WAV / zero framerate."""
    try:
        with wave.open(BytesIO(data)) as wav:
            framerate = int(wav.getframerate())
            if framerate <= 0:
                return None
            return int(wav.getnframes()) / framerate
    except (wave.Error, EOFError):
        return None


def guard_request_length(data: bytes) -> None:
    """Raise a typed ``ValidationError`` if ``data`` is a WAV longer than a single request allows."""
    secs = wav_seconds(data)
    if secs is not None and secs > MAX_REQUEST_SECONDS:
        msg = (
            f"Audio is ~{secs:.0f}s; a single transcription request is limited to "
            f"{MAX_REQUEST_SECONDS}s. Use Kora.transcribe or AethexAI.transcribe_audio, "
            f"which auto-chunk long WAV."
        )
        detail = [
            {
                "type": "too_long",
                "loc": ["body", "file"],
                "msg": msg,
                "input": None,
            }
        ]
        raise ValidationError(
            message=msg,
            code="validation_error",
            status_code=422,
            response={
                "error": "Validation failed",
                "code": "validation_error",
                "request_id": None,
                "detail": detail,
                "fields": detail,
            },
        )


def coerce_to_bytes(file: bytes | BinaryIO | File | None) -> bytes | None:
    """Read ``file`` into bytes for bytes / stream / ``File`` input, or ``None`` if unreadable."""
    try:
        if isinstance(file, (bytes, bytearray)):
            return bytes(file)
        if isinstance(file, File):
            return file.payload.read()
        if file is not None:
            return file.read()
    except Exception:
        return None
    return None
