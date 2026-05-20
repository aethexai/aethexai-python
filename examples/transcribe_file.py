"""Transcribe an audio file synchronously and via the async batch flow.

Aethex AI — official SDK examples.

This example exercises both transcription delivery modes available on
:class:`aethexai.AethexAI`:

  * ``transcribe_audio(body=...)`` — synchronous: the server holds the
    connection open until the full transcript is ready, then returns it
    along with metadata (detected language, duration, segments, etc.).

  * ``transcribe_audio_async(body=...)`` — submits a job and returns a
    handle immediately. The caller polls ``get_transcription_job(job_id)``
    until the job reaches a terminal status.

Both modes accept an optional ``language`` hint that biases recognition
when you already know what language the file is in. Leave it unset to
let the server auto-detect.

This example does **not** download an audio sample for you. You must
point ``AUDIO_FILE`` at a file you already have on disk
(``.wav``/``.mp3``/``.m4a``/``.flac`` and similar are supported).

Run::

    export AETHEX_API_KEY=ae_live_...
    export AUDIO_FILE=/path/to/your/audio.wav
    uv run python examples/transcribe_file.py

Required environment variables:

  * ``AETHEX_API_KEY`` — your Aethex API key.
  * ``AUDIO_FILE``     — absolute path to an audio file on disk.

Optional:

  * ``AETHEX_BASE_URL`` — override the API base URL.
  * ``TRANSCRIBE_LANGUAGE`` — language hint, e.g. ``en``, ``fr``.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any

from aethexai import AethexAI
from aethexai._generated.models.body_transcribe_async_api_v1_transcribe_async_post import (
    BodyTranscribeAsyncApiV1TranscribeAsyncPost,
)
from aethexai._generated.models.body_transcribe_sync_api_v1_transcribe_post import (
    BodyTranscribeSyncApiV1TranscribePost,
)
from aethexai._generated.types import UNSET, File

MAX_POLL_SECONDS = 300
POLL_INTERVAL = 3
TERMINAL_STATUSES = {"completed", "succeeded", "failed", "cancelled", "error"}


def _build_file(path: Path) -> File:
    """Open an audio file and wrap it in the generated multipart ``File`` type."""
    return File(
        payload=path.open("rb"),
        file_name=path.name,
        mime_type="audio/wav" if path.suffix.lower() == ".wav" else None,
    )


def transcribe_sync(client: AethexAI, audio_path: Path, *, language: str | None) -> Any:
    """Synchronous transcription — returns the full transcript inline."""
    body = BodyTranscribeSyncApiV1TranscribePost(
        file=_build_file(audio_path),
        language=language if language else UNSET,
    )
    return client.transcribe_audio(body=body)


def transcribe_async_with_polling(
    client: AethexAI,
    audio_path: Path,
    *,
    language: str | None,
    max_seconds: int = MAX_POLL_SECONDS,
) -> Any:
    """Submit an async transcription job, poll until it reaches a terminal status."""
    body = BodyTranscribeAsyncApiV1TranscribeAsyncPost(
        file=_build_file(audio_path),
        language=language if language else UNSET,
    )
    job = client.transcribe_audio_async(body=body)
    job_id = getattr(job, "id", None) or getattr(job, "job_id", None)
    if not job_id:
        raise RuntimeError(
            f"transcribe_audio_async returned no usable id; got {job!r}"
        )
    print(f"  submitted async job: {job_id}")

    deadline = time.monotonic() + max_seconds
    last_status: str | None = None
    while time.monotonic() < deadline:
        snapshot = client.get_transcription_job(job_id)
        status = (
            getattr(snapshot, "status", None)
            or getattr(snapshot, "state", None)
            or "unknown"
        )
        if status != last_status:
            print(f"  job status: {status}")
            last_status = status
        if str(status).lower() in TERMINAL_STATUSES:
            return snapshot
        time.sleep(POLL_INTERVAL)

    raise TimeoutError(f"transcription job {job_id} did not finish in {max_seconds}s")


def _print_transcript(label: str, result: Any) -> None:
    """Pretty-print whatever transcript shape the server returned."""
    text = (
        getattr(result, "text", None)
        or getattr(result, "transcript", None)
        or getattr(result, "transcription", None)
    )
    detected = getattr(result, "language", None) or getattr(result, "detected_language", None)
    duration = getattr(result, "duration", None) or getattr(result, "duration_seconds", None)
    print(f"[{label}]")
    if detected:
        print(f"  detected language: {detected}")
    if duration:
        print(f"  duration: {duration}s")
    if text:
        excerpt = text if len(str(text)) < 400 else str(text)[:400] + "..."
        print(f"  transcript: {excerpt}")
    else:
        print(f"  raw result: {result!r}")


def main() -> int:
    api_key = os.getenv("AETHEX_API_KEY")
    if not api_key:
        print("error: set AETHEX_API_KEY before running this example", file=sys.stderr)
        return 1

    audio_env = os.getenv("AUDIO_FILE")
    if not audio_env:
        print(
            "error: set AUDIO_FILE to the absolute path of an audio file on disk",
            file=sys.stderr,
        )
        return 1
    audio_path = Path(audio_env).expanduser().resolve()
    if not audio_path.is_file():
        print(f"error: AUDIO_FILE does not exist: {audio_path}", file=sys.stderr)
        return 1

    base_url = os.getenv("AETHEX_BASE_URL", "https://api.aethexai.com")
    language = os.getenv("TRANSCRIBE_LANGUAGE") or None

    with AethexAI(api_key=api_key, base_url=base_url) as client:
        # ── 1. Synchronous ─────────────────────────────────────────────
        print(f"Transcribing (sync) {audio_path.name} ...")
        sync_result = transcribe_sync(client, audio_path, language=language)
        _print_transcript("sync", sync_result)

        # ── 2. Async + polling ─────────────────────────────────────────
        print(f"Transcribing (async) {audio_path.name} ...")
        async_result = transcribe_async_with_polling(
            client, audio_path, language=language
        )
        _print_transcript("async", async_result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
