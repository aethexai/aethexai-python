"""Text-to-speech: one-shot synthesis and chunked streaming.

Aethex AI — official SDK examples.

Demonstrates both delivery modes of the TTS surface:

  * ``synthesize_speech`` — POST ``/api/v1/tts`` returns the full audio
    payload. We persist it as ``OUT_DIR/tts_oneshot.wav``.

  * ``stream_speech`` — POST ``/api/v1/tts/stream`` returns chunked
    PCM16 audio at 24kHz. We write chunks to ``OUT_DIR/tts_stream.pcm``
    as they arrive and print bytes-received progress.

Both call sites use the full :class:`aethexai.AethexAI` client so the
example exercises the general SDK surface rather than the focused Kora
wrapper.

Run::

    export AETHEX_API_KEY=ae_live_...
    uv run python examples/tts_streaming.py

Required environment variables:

  * ``AETHEX_API_KEY`` — your Aethex API key.

Optional:

  * ``AETHEX_BASE_URL`` — override the API base URL.
  * ``TTS_TEXT`` — text to synthesize (default: a short English greeting).
  * ``TTS_VOICE_ID`` — voice id to use (default: ``fatima``).
  * ``TTS_LANGUAGE`` — language code (default: ``english``).
  * ``OUT_DIR`` — directory for output files (default: ``./tts_out``).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from aethexai import AethexAI

DEFAULT_TEXT = "Hello from Aethex, this is a streaming text to speech demo."
DEFAULT_VOICE = "fatima"
DEFAULT_LANGUAGE = "english"


def synthesize_speech(
    client: AethexAI,
    text: str,
    voice_id: str,
    *,
    language: str = DEFAULT_LANGUAGE,
    out_path: Path,
) -> Path:
    """One-shot synthesis: call ``synthesize_speech`` and persist to disk."""
    audio = client.synthesize_speech(
        text=text,
        voice_id=voice_id,
        language=language,
    )
    out_path.write_bytes(audio)
    return out_path


def stream_speech(
    client: AethexAI,
    text: str,
    voice_id: str,
    *,
    language: str = DEFAULT_LANGUAGE,
    out_path: Path,
    chunk_size: int = 4096,
) -> tuple[Path, int]:
    """Stream synthesis: write PCM16 chunks to disk as they arrive.

    Returns the output path and total bytes written.
    """
    total = 0
    with out_path.open("wb") as fh:
        for chunk in client.stream_speech(
            text=text,
            voice_id=voice_id,
            language=language,
            chunk_size=chunk_size,
        ):
            if not chunk:
                continue
            fh.write(chunk)
            total += len(chunk)
            print(f"  received: {total:>10,} bytes", end="\r", flush=True)
    print()
    return out_path, total


def main() -> int:
    api_key = os.getenv("AETHEX_API_KEY")
    if not api_key:
        print("error: set AETHEX_API_KEY before running this example", file=sys.stderr)
        return 1

    base_url = os.getenv("AETHEX_BASE_URL", "https://api.aethexai.com")
    text = os.getenv("TTS_TEXT", DEFAULT_TEXT)
    voice_id = os.getenv("TTS_VOICE_ID", DEFAULT_VOICE)
    language = os.getenv("TTS_LANGUAGE", DEFAULT_LANGUAGE)

    out_dir = Path(os.getenv("OUT_DIR", "./tts_out"))
    out_dir.mkdir(parents=True, exist_ok=True)

    with AethexAI(api_key=api_key, base_url=base_url) as client:
        # ── 1. One-shot ────────────────────────────────────────────────
        oneshot_path = out_dir / "tts_oneshot.wav"
        print(f"Synthesizing one-shot to {oneshot_path} ...")
        synthesize_speech(
            client, text, voice_id, language=language, out_path=oneshot_path
        )
        size = oneshot_path.stat().st_size
        print(f"  wrote {size:,} bytes")

        # ── 2. Chunked streaming ──────────────────────────────────────
        # Output is raw PCM16 mono at 24kHz; play with e.g.
        #   ffplay -f s16le -ar 24000 -ac 1 tts_out/tts_stream.pcm
        stream_path = out_dir / "tts_stream.pcm"
        print(f"Streaming to {stream_path} (raw PCM16 @ 24kHz) ...")
        _, total = stream_speech(
            client, text, voice_id, language=language, out_path=stream_path
        )
        print(f"  stream complete: {total:,} bytes")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
