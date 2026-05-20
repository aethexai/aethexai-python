"""Live WebRTC conversation with an Aethex agent.

Aethex AI — official SDK examples.

Demonstrates the realtime conversation surface exposed by
:class:`aethexai.realtime.Conversation`. The flow is:

  1. Construct an :class:`aethexai.AsyncAethexAI` async client.
  2. Build :class:`aethexai.realtime.ConversationCallbacks` with handlers
     for audio frames, agent text, and status transitions.
  3. Create a :class:`Conversation` bound to an existing ``AGENT_ID``.
  4. ``await conv.start()`` to negotiate the WebRTC PeerConnection.
  5. After a short warm-up, push a text message via ``send_text(...)``
     and inject a context variable via ``inject_context(...)``.
  6. Run for ``CONV_DURATION_SECONDS``, then ``await conv.end()``.

Requires the ``realtime`` extra::

    pip install 'aethexai[realtime]'

Run::

    export AETHEX_API_KEY=ae_live_...
    export AGENT_ID=ag_...
    uv run python examples/realtime_conversation.py

Required environment variables:

  * ``AETHEX_API_KEY`` — your Aethex API key.
  * ``AGENT_ID``       — id of an agent you already created (see
    ``agent_create_and_call.py`` for one way to make one).

Optional:

  * ``AETHEX_BASE_URL``         — override the API base URL.
  * ``CONV_DURATION_SECONDS``   — how long to stay in the conversation
    (default: ``30``).
  * ``CONV_GREETING``           — text message to send mid-conversation.
"""

from __future__ import annotations

import asyncio
import os
import sys

from aethexai import AsyncAethexAI
from aethexai.realtime import Conversation, ConversationCallbacks

DEFAULT_DURATION_SECONDS = 30
DEFAULT_GREETING = "Quick interruption — can you switch to English for the rest of this call?"


async def run_conversation(
    api_key: str,
    base_url: str,
    agent_id: str,
    *,
    duration_seconds: int,
    greeting: str,
) -> int:
    audio_bytes_received = 0

    def on_agent_audio(pcm: bytes) -> None:
        # 48kHz s16 mono PCM. In a real app you would push these frames
        # to an output device, a buffer, or a file.
        nonlocal audio_bytes_received
        audio_bytes_received += len(pcm)

    def on_agent_text(text: str) -> None:
        print(f"[agent] {text}")

    def on_user_transcript(text: str) -> None:
        print(f"[you]   {text}")

    def on_status_change(status: str) -> None:
        print(f"[status] {status}")

    def on_error(exc: Exception) -> None:
        print(f"[error] {type(exc).__name__}: {exc}", file=sys.stderr)

    callbacks = ConversationCallbacks(
        on_agent_audio=on_agent_audio,
        on_agent_text=on_agent_text,
        on_user_transcript=on_user_transcript,
        on_status_change=on_status_change,
        on_error=on_error,
    )

    async with AsyncAethexAI(api_key=api_key, base_url=base_url) as client:
        conv = Conversation(client, agent_id=agent_id, callbacks=callbacks)
        await conv.start()
        print(f"session_id: {conv.session_id}")

        # Give the connection a moment to settle before we start poking
        # the live session with text and context updates.
        await asyncio.sleep(2.0)

        if conv.is_connected:
            print("Sending text message into the live session ...")
            await conv.send_text(greeting)

            print("Injecting context variables ...")
            await conv.inject_context(
                {
                    "customer_name": "Aminata",
                    "account_tier": "premium",
                    "preferred_language": "english",
                }
            )
        else:
            print("warning: data channel not open yet; skipping text/context push")

        # Stay in the call for the configured duration.
        remaining = max(0.0, duration_seconds - 2.0)
        print(f"Holding the line for {remaining:.0f}s ...")
        await asyncio.sleep(remaining)

        await conv.end()
        print(f"received {audio_bytes_received:,} bytes of agent audio")

    return 0


def main() -> int:
    api_key = os.getenv("AETHEX_API_KEY")
    if not api_key:
        print("error: set AETHEX_API_KEY before running this example", file=sys.stderr)
        return 1

    agent_id = os.getenv("AGENT_ID")
    if not agent_id:
        print(
            "error: set AGENT_ID to the id of an existing agent "
            "(see examples/agent_create_and_call.py)",
            file=sys.stderr,
        )
        return 1

    base_url = os.getenv("AETHEX_BASE_URL", "https://api.aethexai.com")
    duration_seconds = int(os.getenv("CONV_DURATION_SECONDS", str(DEFAULT_DURATION_SECONDS)))
    greeting = os.getenv("CONV_GREETING", DEFAULT_GREETING)

    return asyncio.run(
        run_conversation(
            api_key,
            base_url,
            agent_id,
            duration_seconds=duration_seconds,
            greeting=greeting,
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
