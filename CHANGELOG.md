# Changelog

All notable changes to this project are documented here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `cancel_transcription_job` (sync and async) now returns a typed `CancelTranscriptionJobResponse` (`id`, `status`) instead of a raw `dict`, matching the other transcription wrappers. The on-the-wire shape is unchanged, but code that indexed the old dict result (e.g. `result["id"]`) must now use attribute access (`result.id`). (AET-1538)

### Fixed

- 422 responses with the aethex unified error envelope (`{error, code, detail: <string>, request_id}`) now raise the documented `aethexai.ValidationError` instead of crashing inside the generated `HTTPValidationError.from_dict` with `ValueError: dictionary update sequence element #0 has length 1; 2 is required`. The FastAPI-shaped `detail: list[ValidationError]` shape continues to parse. (AET-1523)
- `AethexAI.list_voices`, `AsyncAethexAI.list_voices`, and `Kora.list_voices` now forward the OpenAPI `tag` query parameter (and `supports_dialect_style` for `Kora.list_voices`), which were silently dropped by the wrappers. (AET-1534)

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
