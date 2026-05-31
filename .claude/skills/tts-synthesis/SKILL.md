---
name: tts-synthesis
description: >-
  Text-to-speech (TTS) with the AethexAI Python SDK. Use when asked to
  "synthesize speech", do "text to speech" / "TTS", "turn text into audio",
  "generate a voiceover / WAV", "list available voices", "browse the voice
  catalog", "look up voice tags", "preview / audition a voice", or "stream audio
  from text". Covers the voice catalog (list_voices, get_voice,
  list_tag_vocabulary), voice previews (preview_voice -> WAV bytes), one-shot
  synthesis (synthesize_speech -> WAV bytes), and low-latency streaming
  (stream_speech -> raw PCM chunks) on the sync AethexAI client.
tools: Read, Edit, Bash
---

# TTS synthesis (AethexAI)

What this does: generate spoken audio from text using the AethexAI sync client
(`AethexAI`, `src/aethexai/client.py`). It covers discovering a voice from the
catalog, auditioning a voice with a short preview, one-shot synthesis to a WAV
file, and chunked streaming for low latency.

When to use: any request to convert text to speech, produce a `.wav`, pick or
list voices, inspect the voice tag vocabulary, or stream audio as it is
generated.

The same methods exist on `AsyncAethexAI` (`src/aethexai/_async_client.py`) with
identical signatures (await them; `stream_speech` becomes an async iterator).

## Construct the client

```python
from aethexai import AethexAI

client = AethexAI(api_key="ak_live_...")  # or omit and set AETHEX_API_KEY
```

## Voice catalog

`list_voices(...)` returns a **bare `list[VoiceResponse]`** (not a wrapper —
iterate it directly). All filters are keyword-only:

```python
list_voices(
    *,
    language: str | None = UNSET,        # UNSET = omit the filter; lowercase, e.g. "english"
    supports_dialect_style: bool | None = UNSET,
    tag: str | None = UNSET,             # any token from list_tag_vocabulary()
    limit: int = 100,
    offset: int = 0,
)  # wrapper's static return is `Any`; at runtime you get a list[VoiceResponse]
```

Each `VoiceResponse` exposes: `.id`, `.name`, `.language`, `.gender`,
`.is_cloned` (bool), `.supports_dialect_style` (bool), `.tags` (`list[str]`),
`.description`, and `.preview_url`. (The model also declares a `voice_type`
field — declared default `"icl"` — but the live API omits it, so parsed voices
carry `Unset` for it; don't rely on it.)

```python
voices = client.list_voices(language="english", limit=10)
for v in voices:
    print(v.id, v.name, v.language, v.gender)

# Fetch one voice by id:
voice = client.get_voice(voices[0].id)
print(voice.name, voice.tags)
```

`list_tag_vocabulary()` returns the closed tag vocabulary, grouped into four
buckets: `tone`, `voice_texture`, `delivery_style`, `business_persona`. The
result is a dict-like object — index it by bucket name to get a `list[str]` of
tags. Any token from any bucket is valid for `list_voices(tag=...)`.

```python
vocab = client.list_tag_vocabulary()
print(vocab["tone"])            # e.g. ["warm", "energetic", ...]
print(dict(vocab.additional_properties))  # all four buckets at once

# Then filter the catalog by a discovered tag:
warm_voices = client.list_voices(tag="warm")
```

## Preview / audition a voice -> WAV bytes

`preview_voice(voice_id=, text=) -> bytes` returns a short sample clip of a voice
as a complete **WAV** (same PCM16, mono, 24 kHz container as
`synthesize_speech`). Use it to audition a voice from the catalog before
committing to full synthesis. `voice_id` is required; `text` is optional and
defaults server-side to `"Hello, this is a sample of my voice."`.

```python
voice = client.list_voices(language="english", limit=1)[0]

sample = client.preview_voice(voice_id=voice.id)                       # default sample text
sample = client.preview_voice(voice_id=voice.id, text="Hi, I'm Ada.")  # or custom text

with open("preview.wav", "wb") as f:
    f.write(sample)  # already a valid WAV file
```

## One-shot synthesis -> WAV bytes

`synthesize_speech(text=, voice_id=, language=) -> bytes`. The returned bytes
are a complete **WAV container** (PCM16, mono, 24 kHz) — write them straight to
a `.wav` file, no header work required.

```python
voice = client.list_voices(language="english", limit=1)[0]

audio = client.synthesize_speech(
    text="Hello from AethexAI.",
    voice_id=voice.id,
    language="english",
)

with open("out.wav", "wb") as f:
    f.write(audio)  # already a valid WAV file
```

`text` is the only required field; `language` defaults to `"english"` and
`voice_id` is optional (a default voice is used if omitted), but passing a real
voice id is recommended.

## Streaming -> raw PCM16 chunks

`stream_speech(chunk_size=4096, text=, voice_id=, language=) -> Iterator[bytes]`
yields audio as it is generated for low time-to-first-byte (TTFB ~382 ms).

Important: streamed chunks are **RAW PCM16, mono, 24 kHz with NO WAV header**
(unlike `synthesize_speech`, which is a full WAV). If you need a playable
`.wav`, wrap the concatenated PCM yourself. `chunk_size` is keyword-only and
controls the byte size of each yielded chunk.

```python
import wave

voice = client.list_voices(language="english", limit=1)[0]

pcm = bytearray()
for chunk in client.stream_speech(
    text="Streaming speech, chunk by chunk.",
    voice_id=voice.id,
    language="english",
    chunk_size=4096,
):
    pcm.extend(chunk)  # raw PCM16 — play live, or buffer to wrap below

# Wrap the raw PCM in a WAV header to get a playable file:
with wave.open("stream_out.wav", "wb") as w:
    w.setnchannels(1)        # mono
    w.setsampwidth(2)        # PCM16 = 2 bytes/sample
    w.setframerate(24000)    # 24 kHz
    w.writeframes(bytes(pcm))
```

## Gotchas

- Language args are **lowercase strings**: `"english"`, `"french"` (not
  `"English"` or locale codes).
- **Warm-up penalty:** the first TTS call after startup is slower (~4 s) than
  steady-state (~2 s). Budget for it or issue a throwaway warm-up call.
- `synthesize_speech` -> full WAV bytes (write directly).
  `stream_speech` -> headerless raw PCM16 chunks (you must add a WAV header, as
  shown above, to get a playable file).
- `list_voices` returns a plain list, so `voices[0]`, slicing, and `len()` all
  work; there is no `.data` attribute on it.
- **Errors are typed.** Any non-2xx maps to the `aethexai` exception hierarchy
  (`AuthenticationError`, `ValidationError`, `RateLimitError`,
  `InternalServerError`, …); transport failures raise
  `APIConnectionError`/`APITimeoutError`. A missing required field — `text` for
  `synthesize_speech`, `voice_id` for `preview_voice` — raises `ValidationError`
  *before* the request is sent.
- **`stream_speech` is a lazy generator.** Nothing is sent until you iterate it,
  so an initial-response error (401/422/429/5xx) surfaces on the **first**
  `for chunk in …`, not at the `stream_speech(...)` call site — start consuming
  the iterator inside your `try/except`.

See CLAUDE.md for repo-working context (install with `uv sync --extra dev`,
tests via `uv run pytest -m "not integration"`, lint with `uv run ruff check .`,
and async parity on `AsyncAethexAI`).
