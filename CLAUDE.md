# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## What this is

`aethexai` is the official Python SDK for the **Aethex voice AI platform** (TTS, ASR/transcription, voice agents, calls, conversations). Src layout under `src/aethexai/`, Python >=3.10, built with **uv + hatchling**. The package exposes three clients:

- **`AethexAI`** (sync, `client.py`) and **`AsyncAethexAI`** (`_async_client.py`) — the full flat-method API surface, kept in sync/async parity. Constructor: `AethexAI(api_key=None, *, base_url=..., timeout=30.0, max_retries=2, httpx_client=None)`; `api_key` falls back to the `AETHEX_API_KEY` env var, and a missing key raises `AuthenticationError`.
- **`Kora`** (`kora.py`) — a focused voice client (agents, calls, voices, TTS, transcription, read-only conversation history). Positional constructor: `Kora(base_url, api_key)`.

## GENERATED vs HAND-WRITTEN (read first)

**NEVER edit `src/aethexai/_generated/`.** It is produced by `openapi-python-client` from the backend OpenAPI spec and is excluded from ruff + mypy (see `[tool.ruff] extend-exclude` and `[tool.mypy] exclude` in `pyproject.toml`). Any manual edit there is destroyed on the next regen.

Regenerate the generated layer with:

```bash
uv run python scripts/dump_openapi.py     # writes openapi.json from the backend
uv run python scripts/sync_from_prod.py   # regenerates _generated/ + reapplies post-codegen patches
```

`sync_from_prod.py` re-applies a series of post-codegen patches (comment stripping, HTTP validation-error handling, 201-created parsing, paginated-list ergonomics, typed AgentResponse parsing, any-2xx success branch). **These patches must survive regen** — they are guarded by `tests/test_sync_patch_durability.py` and `tests/test_paginated_response_regen_durability.py`. If you change patch logic, run those tests.

**Hand-written surface (edit these):** `client.py`, `_async_client.py`, `kora.py`, `_exceptions.py`, `_body.py`, `__init__.py`, `realtime/`.

## Commands

```bash
# Install (contributors)
uv sync --all-extras --dev        # everything incl. the realtime extra
uv sync --extra dev               # skip the realtime extra

# Tests
uv run pytest                     # full suite
uv run pytest -m "not integration"  # default unit run (no live API)
uv run pytest -m integration      # needs AETHEX_API_KEY + live API
uv run pytest -m slow             # longer-running tests

# Lint / format
uv run ruff check .
uv run ruff format .

# Types
uv run mypy src/aethexai
```

The only optional extras that exist are `realtime` and `dev`.

## Architecture

- **Flat method API.** Every operation is a top-level method — `client.create_agent(...)`, `client.list_calls(...)`, `client.synthesize_speech(...)` — with no nested `client.agents.create(...)` namespaces.
- **Every wrapper funnels through `_call()`.** It runs the generated `*.sync_detailed` / `*.asyncio_detailed` op, returns `response.parsed` on 2xx, and on any non-2xx raises a typed exception via `_map_status_to_exception` (`_exceptions.py`). Network/timeout failures become `APIConnectionError` / `APITimeoutError`.
- **Bodies go through `build_body()`** (`_body.py`). It pre-validates required fields against the model's attrs definition and raises a typed `ValidationError` listing **all** missing fields (with a server-shaped `detail`/`fields` payload) before the request goes out — instead of a bare `KeyError` from `from_dict`. It also maps keyword-suffixed attr names (`type_` -> `type`) back to wire names.
- **Sync/async parity is mandatory.** `AethexAI` and `AsyncAethexAI` must stay method-for-method identical (signatures, body shaping, URL templating, parsing). Enforced by `tests/test_async_parity.py`.

## Return-type contract

- **Typed models** for resource reads/writes: `AgentResponse`, `CallResponse`, `ConversationResponse`, and `PaginatedResponse[T]`.
- **`dict`** for open-ended payloads (usage / billing).
- **`bytes`** for audio (`synthesize_speech`, `preview_voice`, `stream_audio`, `Kora.get_conversation_audio`).
- **`create_agent` returns a typed `AgentResponse`** — use attribute access `agent.id`, never `agent["id"]`. Guarded by `tests/test_typed_agent_responses.py` and durable across regen.
- **Bare lists:** `list_voices` and `list_api_keys` return plain lists.
- **Paginated** (`{data, total, limit, offset}`): `list_agents`, `list_calls`, `list_conversations`, `list_phone_numbers`, `list_twilio_accounts`. `PaginatedResponse` has a `.has_more` property and integer indexing; iterate `.data` and loop while `.has_more` to consume every page (it has no `__iter__`/`__len__`).
- **Long audio (>~35s)** is auto-chunked client-side by the sync `Kora.transcribe` and `AethexAI.transcribe_audio` paths. With the optional `audio` extra (PyAV) installed, any input — bytes / stream / `File`, WAV or otherwise (mp3/m4a/stereo/48k) — is first normalized to canonical 24kHz mono 16-bit PCM WAV; without the extra it falls back to WAV-only and sends non-canonical input as-is. The normalized audio is split on silence at ≤30s boundaries (a margin under the 35s per-request cap) so words aren't cut mid-syllable, transcribed per chunk, and concatenated as space-joined text (chunks are contiguous/non-overlapping, so no seam de-duplication is needed). The backend returns no segments, so the merge is text-based. The inline async routes (`transcribe_async`, `transcribe_audio_async`) have the bytes locally and raise a typed `ValidationError` for a >35s WAV (pointing at the auto-chunking sync paths); the by-upload routes only get an `upload_id`, so they're server-bound and surface the ~35s per-request limit directly. Helpers live in `_transcription.py` (`CHUNK_SECONDS=30`, `MAX_REQUEST_SECONDS=35`).

## Errors

Typed hierarchy rooted at `AethexError` (`_exceptions.py`):

- `AuthenticationError` (401), `PermissionDeniedError` (403), `NotFoundError` (404), `ConflictError` (409)
- `ValidationError` (422, exposes `.response`), `RateLimitError` (429, exposes `.retry_after`)
- `InternalServerError` (5xx)
- `APIConnectionError` and `APITimeoutError` for transport/timeout failures.

All status-derived errors are `APIStatusError` subclasses carrying `message`, `code`, `status_code`, `response`, `headers`.

## "Purely external" invariant

Published artifacts must contain **no internal references** (internal routes, infra nouns, ticket numbers, internal table/header names, audit-doc references, internal GitHub usernames). Enforced by `tests/test_no_internal_leak.py`. The sdist deliberately ships only customer-facing files (see `[tool.hatch.build.targets.sdist]` — `scripts/`, `tests/`, `.github`, docs are excluded).

## Realtime extra

`uv sync --extra realtime` installs `aiortc` + `aioice` + `av` (PyAV); the version constraints resolve `av` to `14.2.0`, the newest 14.x with binary wheels, so supported Pythons install **without a system FFmpeg build**. After that, `from aethexai.realtime import Conversation, ConversationCallbacks` works. A live WebRTC call is untested — treat realtime as install + import verified only.

## Verified read / audio-access surface

(One-liners, not exhaustive.) Usage reads: `get_usage`, `get_usage_summary`, `get_daily_usage`, `get_monthly_usage`. Catalog: `list_models`. Resource reads: agent / call / conversation getters and lists. `search_conversations(q, *, limit=20)`. Conversation playback: `get_audio` / `revoke_audio_token` (the playback token rides in the returned URL's query string); `stream_audio` returns WAV bytes. On `Kora`: `get_conversation_audio` / `get_conversation_audio_url` / `get_conversation_transcript`. All of the above have verified sync/async parity.

## Contributing + release

- Branch off `main` with a prefix: `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`.
- Adding a flat method requires a **respx unit test** under `tests/` (e.g. `tests/test_aethexai_methods.py`, `tests/test_kora_methods.py`), and — if it lands on `AethexAI` — a matching `AsyncAethexAI` method to keep parity (`tests/test_async_parity.py`).
- Record user-facing changes in `CHANGELOG.md` under `## [Unreleased]`.
- **Releases are tag-driven:** bump `src/aethexai/_version.py` + `version` in `pyproject.toml`, move the `[Unreleased]` CHANGELOG entries under the new version, `git tag -a vX.Y.Z`, push the tag — CI publishes to PyPI via trusted publishing.

## Doc-drift caution

Prefer `pyproject.toml` + real file paths over `CONTRIBUTING.md` prose. `CONTRIBUTING.md` is stale: it references a non-existent `websocket` extra and a `tests/test_kora.py` file. The real extras are `realtime` and `dev`; the real Kora test file is `tests/test_kora_methods.py`.

## SDK usage flows

`.claude/skills/` contains verified SDK usage flows — `tts-synthesis`, `audio-transcription`, `agents-and-knowledge-base`. Consult those for copy-paste usage examples; this file is repo-working guidance, not an SDK tutorial.
