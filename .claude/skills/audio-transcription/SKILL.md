---
name: audio-transcription
description: Transcribe audio to text (speech-to-text / ASR) with the AethexAI Python SDK. Use this when you need to transcribe an audio file, run speech recognition, get a transcript from a recording, submit a transcription job and poll it, or upload a file to storage first and then transcribe it. Covers the simple Kora.transcribe path, the async submit-and-poll job lifecycle, and the presigned-upload (transcribe-by-upload) path on the AethexAI client.
---

# Audio transcription (speech-to-text / ASR)

Convert audio (WAV, etc.) into text. There are two ways to do it:

- **Path A — Kora (simple):** hand the SDK the raw bytes or a file object. Best for the common case.
- **Path B — presigned upload (AethexAI client):** PUT the file straight to storage, then transcribe by `upload_id`. Use this when the file is large or already lives in/needs to live in object storage.

Each path has a **sync** variant (blocks, returns the transcript) and an **async** variant (returns a job handle immediately; you poll until done, or supply a webhook). The async transcript is identical to the sync transcript — sync is faster and simpler for short clips; async (or `webhook_url`) is for long recordings that would exceed a sync request timeout.

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
- **Sync vs async:** sync is faster and simpler for short clips (under ~1-2 min). Use async (or `webhook_url`) for long recordings that would otherwise exceed the sync request timeout.
- **Async returns immediately, then polls.** A fresh job's `.status` starts at `"pending"`; `.text` is empty until `.status == "completed"`. Always check status before reading text.
- **Weak ASR spots.** Brand names and numerals are the least reliable parts of a transcript (overall WER ~5.3%). Expect occasional misspellings of product/brand names and digits.
- **Terminal statuses are `completed` / `failed` / `cancelled`.** If a job can be cancelled (by you via `cancel_transcription_job`, or by another caller), include `"cancelled"` in your poll loop's terminal check or it will spin forever. `cancel_transcription_job` returns a minimal object (`.id`, `.status == "cancelled"`) — no `.text`.
- **Uploads are size-capped (~8 MiB).** `presign_upload` returns `.max_bytes` (verified 8388608); an over-size PUT is rejected at the storage layer, not via a typed SDK error — check `len(data) <= presigned.max_bytes` before the PUT.

---

See CLAUDE.md for repo-working context (install, tests, client routing, and conversation-playback access like `get_audio`/`revoke_audio_token`, which are separate from transcription).
