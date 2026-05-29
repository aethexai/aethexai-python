# Changelog

All notable changes to this project are documented here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] — 2026-05-29

### Changed

- **All JSON-returning client methods now return the decoded response body as a plain `dict` / `list`** (or `None` for an empty `2xx` response) instead of a generated model instance. This keeps the SDK's return contract stable regardless of whether the backend declares a response schema for a route — or changes a route's success status code — and removes generated model types from the public surface. Binary / audio methods (`synthesize_speech`, `preview_voice`, `stream_speech`, `stream_audio`, `get_conversation_audio`, `get_recording_audio`) are unaffected and still return `bytes`.

  **Migration:** replace attribute access on results with key access — `agent.id` → `agent["id"]`, `result.batch_id` → `result["batch_id"]`, `page.data` → `page["data"]`.

- Responses are decoded directly from the raw `2xx` body, so resource-creation POSTs that return `200` **or** `201` both reliably yield the created resource (never `None`) with no per-status special-casing.

### Added

- `list_tag_vocabulary()` (sync and async) — wrapper for `GET /api/v1/voices/tag-vocabulary`. Returns the closed tag vocabulary (tone, voice texture, delivery style, business persona) accepted by `list_voices(tag=...)`.

### Fixed

- `select_plan()` (sync and async) no longer raises `TypeError: Object of type Unset is not JSON serializable` when called without a body. `body` now defaults to `None`; the natural `select_plan("pro")` call issues the POST with no JSON body and the server defaults to monthly billing. Pass a body to choose a different interval.
- Missing required body fields on POST wrappers (e.g. `create_agent`, `presign_upload`, `trigger_call`) now raise a typed `aethexai.ValidationError` listing every missing field, instead of a stdlib `KeyError` that reported only the first. The request still short-circuits before the wire call, and the error envelope mirrors the server's `422` shape so one handler covers both SDK pre-flight and server-side validation errors.
- `422` responses carrying the unified error envelope (`{error, code, detail, request_id}`) now raise the documented `aethexai.ValidationError` instead of crashing inside response parsing.
- `list_voices` (all clients) now forwards the `tag` query parameter (and `supports_dialect_style` on `Kora.list_voices`), which were previously dropped by the wrappers.
- Binary audio endpoints no longer crash with `UnicodeDecodeError` on a successful response; they return raw `bytes` across `AethexAI`, `AsyncAethexAI`, and `Kora`.
- Method docstrings link to the correct documentation domain (`https://developers.aethexai.com/docs/...`).

### Security & packaging

- The published package is now strictly customer-facing. Internal and operational endpoints (admin routes, health probes, metrics) are excluded from the bundled `openapi.json` and the generated client, and internal commentary (issue references, internal table names, infrastructure notes, internal auth-header names) is scrubbed from every shipped docstring.
- The source distribution ships only the package, `openapi.json`, `README`, `LICENSE`, and `CHANGELOG`; internal tooling and the test suite are no longer included.

## [0.2.1] — 2026-05-20

Initial release.

The Aethex AI Python SDK provides synchronous and asynchronous clients for the [Aethex voice AI platform](https://aethexai.com).

### Clients

- **`AethexAI`** / **`AsyncAethexAI`** — full-surface clients for the Aethex API, authenticated with `X-API-Key`. Cover agents, voices, calls, conversations, transcription, text-to-speech, phone numbers, SIP trunks, recordings, models, and usage.
- **`Kora`** — voice-focused subset for building voice agents quickly: agents, outbound calls, voices, text-to-speech, transcription, and read-only conversation history.
- **`DeveloperClient`** / **`AsyncDeveloperClient`** — JWT-authenticated clients for billing and account endpoints. Carry `Authorization: Bearer <jwt>` and auto-refresh on 401 when a refresh token is provided. Tokens come from the magic-link or Google sign-in flow at [developers.aethexai.com](https://developers.aethexai.com).

### Features

- Real-time WebRTC `Conversation` (install with `pip install aethexai[realtime]`).
- Typed exception hierarchy mapped to HTTP status codes: `AuthenticationError`, `PermissionDeniedError`, `NotFoundError`, `ConflictError`, `ValidationError`, `RateLimitError`, `InternalServerError`, `APIConnectionError`, `APITimeoutError`.
- Full async parity — every sync method has an async equivalent.
- Type hints throughout (`py.typed`).
- Python 3.10 through 3.13 supported.
