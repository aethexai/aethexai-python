---
name: audio-transcription
description: Transcribe audio to text (speech-to-text / ASR) with the AethexAI Python SDK. Use this when you need to transcribe an audio file, run speech recognition, get a transcript from a recording, submit a transcription job and poll it, or upload a file to storage first and then transcribe it. Covers the simple Kora.transcribe path, the async submit-and-poll job lifecycle, and the presigned-upload (transcribe-by-upload) path on the AethexAI client.
---

# Audio transcription (speech-to-text / ASR)

Convert audio (WAV, etc.) into text. There are two ways to do it:

- **Path A — Kora (simple):** hand the SDK the raw bytes or a file object. Best for the common case.
- **Path B — presigned upload (AethexAI client):** PUT the file straight to storage, then transcribe by `upload_id`. Use this when the file is large or already lives in/needs to live in object storage.

Each path has a **sync** variant (blocks, returns the transcript) and an **async** variant (returns a job handle immediately; you poll until done, or supply a webhook). The async transcript is identical to the sync transcript. The backend caps a single transcription request at ~35s; `Kora.transcribe` and `AethexAI.transcribe_audio` transparently handle longer recordings client-side: they normalize input (bytes / stream / `File`) to canonical 24kHz mono 16-bit WAV, split it on silence at ≤30s boundaries (a margin under the cap, chosen so words aren't cut mid-syllable), transcribe each chunk, and concatenate the transcripts. With the optional `aethexai[audio]` extra (PyAV) installed, normalization accepts any format (mp3, m4a, stereo or 48kHz WAV, etc.); without it the paths handle WAV only and send non-canonical input as-is. The backend returns no segments, so the merge is text-based. The inline async-job paths (`transcribe_async`, `transcribe_audio_async`) do **not** chunk and raise a typed `aethexai.ValidationError` client-side when handed a WAV longer than ~35s, pointing you to the auto-chunking `Kora.transcribe` / `AethexAI.transcribe_audio` instead of the opaque server error. The by-upload paths only receive an `upload_id` (no local bytes), so they can't be guarded and surface the server's ~35s limit directly. Async is for fire-and-forget / webhook delivery, **not** for getting around length limits.

Language arguments are lowercase strings: `"english"`, `"french"`.

---

## Path A — Kora (simple)

`Kora` is the focused voice client. Its constructor is **positional**: `Kora(base_url, api_key)`.

```python
import os
from aethexai import Kora

kora = Kora("https://api.aethexai.com", os.environ["AETHEX_API_KEY"])
```

### Sync — `Kora.transcribe(...)`

```python
def transcribe(
    self,
    file: bytes | BinaryIO | File,
    *,
    language: str | None = None,
    file_name: str | None = None,
    mime_type: str | None = None,
) -> Any  # transcript object with .text, .id, .language, .duration_seconds
```

```python
with open("call.wav", "rb") as f:
    result = kora.transcribe(
        f,
        language="english",
        file_name="call.wav",
        mime_type="audio/wav",
    )

print(result.text)
```

You can also pass raw bytes directly: `kora.transcribe(b"...wav bytes...", language="english", file_name="call.wav", mime_type="audio/wav")`.

### Async — `Kora.transcribe_async(...)` then poll `Kora.get_transcribe_job(...)`

`transcribe_async` returns a **job handle immediately** (with `.id` and `.status`). Poll `get_transcribe_job(job_id)` until `job.status` is terminal (`"completed"` or `"failed"`), then read `job.text`.

```python
def transcribe_async(
    self,
    file: bytes | BinaryIO | File,
    *,
    language: str | None = None,
    webhook_url: str | None = None,
    file_name: str | None = None,
    mime_type: str | None = None,
) -> Any  # job handle: .id, .status, .text (filled once completed)

def get_transcribe_job(self, job_id: str | UUID) -> Any
```

```python
import os, time
from aethexai import Kora

kora = Kora("https://api.aethexai.com", os.environ["AETHEX_API_KEY"])

with open("long-call.wav", "rb") as f:
    job = kora.transcribe_async(
        f,
        language="english",
        file_name="long-call.wav",
        mime_type="audio/wav",
    )

while job.status not in ("completed", "failed", "cancelled"):
    time.sleep(1)
    job = kora.get_transcribe_job(job.id)

if job.status == "completed":
    print(job.text)
else:
    print("transcription failed")
```

Pass `webhook_url="https://your.app/hook"` to `transcribe_async` to be notified on completion instead of polling.

---

## Path B — presigned upload (AethexAI client)

Use this when you want to upload the file directly to object storage (it bypasses the API for the byte transfer), then transcribe it by reference. The flow is: **presign -> PUT bytes -> transcribe by upload_id**.

```python
import os
from aethexai import AethexAI

client = AethexAI(api_key=os.environ["AETHEX_API_KEY"])  # or rely on AETHEX_API_KEY
```

### 1. `presign_upload(...)`

```python
def presign_upload(self, **fields: Any) -> Any
# fields: content_type=str, kind=str, filename=str|None, size_hint=int|None
# returns: .upload_id (single-use signed JWT), .upload_url, .method ("PUT"),
#          .max_bytes, .headers, .expires_at
```

For transcription consumers, pass `kind="audio/transcribe"`.

### 2. PUT the raw bytes to `upload_url`

This is a plain `httpx` PUT directly to storage — it does **not** go through the AethexAI client.

```python
import httpx

data = open("call.wav", "rb").read()

presigned = client.presign_upload(
    content_type="audio/wav",
    kind="audio/transcribe",
    filename="call.wav",
    size_hint=len(data),
)

put = httpx.put(
    presigned.upload_url,
    content=data,
    headers={"Content-Type": "audio/wav"},
)
put.raise_for_status()
```

### 3. Transcribe by `upload_id`

Sync:

```python
def transcribe_audio_by_upload(self, **fields: Any) -> Any
# fields: upload_id=str, language=str|None  -> transcript object with .text
```

```python
result = client.transcribe_audio_by_upload(
    upload_id=presigned.upload_id,
    language="english",
)
print(result.text)
```

Async (submit-and-poll), using `get_transcription_job` to poll and `cancel_transcription_job` to abort:

```python
def transcribe_audio_async_by_upload(self, **fields: Any) -> Any
# fields: upload_id=str, language=str|None, webhook_url=str|None -> job handle

def get_transcription_job(self, job_id: str | UUID) -> Any
def cancel_transcription_job(self, job_id: str | UUID) -> Any  # -> status "cancelled"
```

```python
import time

job = client.transcribe_audio_async_by_upload(
    upload_id=presigned.upload_id,
    language="english",
)

while job.status not in ("completed", "failed", "cancelled"):
    time.sleep(1)
    job = client.get_transcription_job(job.id)

print(job.text)

# To abort an in-flight job:
# cancelled = client.cancel_transcription_job(job.id)  # cancelled.status == "cancelled"
```

> The async poll method differs by client: on the **AethexAI** client it is `get_transcription_job(...)`; on **Kora** it is `get_transcribe_job(...)`. They are not interchangeable.

---

## Gotchas

- **`upload_id` is single-use.** It's a signed JWT consumed by one transcribe call. Call `presign_upload` once per transcription — don't reuse an `upload_id` across calls.
- **`kind` matters for uploads.** Use `kind="audio/transcribe"` for files you intend to transcribe.
- **Async output == sync output.** Same ASR backend, identical transcript. Async only changes the operational model (connection released after submit, optional webhook), not the result.
- **Sync vs async:** both call the same ~35s-per-request backend; async does not raise the length limit. The sync `Kora.transcribe` / `AethexAI.transcribe_audio` paths normalize and auto-chunk long recordings (≤30s silence-aware chunks; any format with the `audio` extra, WAV-only without), so use sync for long audio. The inline async paths (`transcribe_async`, `transcribe_audio_async`) raise a typed `aethexai.ValidationError` client-side for a WAV over ~35s, telling you to use the auto-chunking sync paths instead of failing with the opaque server error; the by-upload paths only have an `upload_id` (no local bytes) and so still surface the server's length limit directly. Use async (or `webhook_url`) when you want fire-and-forget / webhook delivery, not to get around length limits.
- **Async returns immediately, then polls.** A fresh job's `.status` starts at `"pending"`; `.text` is empty until `.status == "completed"`. Always check status before reading text.
- **Weak ASR spots.** Brand names and numerals are the least reliable parts of a transcript (overall WER ~5.3%). Expect occasional misspellings of product/brand names and digits.
- **Terminal statuses are `completed` / `failed` / `cancelled`.** If a job can be cancelled (by you via `cancel_transcription_job`, or by another caller), include `"cancelled"` in your poll loop's terminal check or it will spin forever. `cancel_transcription_job` returns a minimal object (`.id`, `.status == "cancelled"`) — no `.text`.
- **Uploads are size-capped (~8 MiB).** `presign_upload` returns `.max_bytes` (verified 8388608); an over-size PUT is rejected at the storage layer, not via a typed SDK error — check `len(data) <= presigned.max_bytes` before the PUT.

---

## Long audio (>35 s)

- **The backend caps each transcription request at ~35s.** A single request to the ASR backend rejects audio longer than that — async does not change this limit.
- **Sync just works.** The sync `Kora.transcribe(open("long.wav", "rb"))` and `AethexAI.transcribe_audio(body=...)` paths normalize input (bytes / stream / `File`) to canonical 24kHz mono 16-bit WAV, split it on silence at ≤30s boundaries client-side, and concatenate the transcripts, so long recordings need no special handling. The ≤30s chunk size is a deliberate margin under the ~35s cap, and seams are chosen at low-energy points so words aren't cut mid-syllable.
- **Format conversion needs the `audio` extra.** Install `pip install "aethexai[audio]"` (PyAV) and non-WAV input (mp3, m4a, etc.) and odd WAV (stereo, 48kHz) are decoded/normalized to canonical 24kHz mono 16-bit WAV before chunking. Without the extra, only WAV is handled and non-canonical input is sent as-is; pre-transcode or pre-split such input yourself in that case.
- **Merge is text-based — no segments.** The backend returns no per-segment timestamps for these requests, so chunk transcripts are concatenated as space-joined text, not stitched by timestamp. Don't rely on `.segments` for chunked audio.
- **Inline async paths reject long WAV with a typed error.** `transcribe_async` / `transcribe_audio_async` do not chunk; handed a WAV longer than ~35s they raise a typed `aethexai.ValidationError` client-side telling you to use the auto-chunking `Kora.transcribe` / `AethexAI.transcribe_audio` instead of failing with the opaque server "Audio too long" error. Use async only for fire-and-forget / webhook delivery, not to handle length.
- **By-upload paths surface the server limit directly.** `transcribe_audio_by_upload` / `transcribe_audio_async_by_upload` only receive an `upload_id` (no local bytes), so they can't be guarded client-side and the ~35s per-request limit is enforced server-side.

---

See CLAUDE.md for repo-working context (install, tests, client routing, and conversation-playback access like `get_audio`/`revoke_audio_token`, which are separate from transcription).
