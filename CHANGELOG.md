# Changelog

All notable changes to this project are documented here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0]

### Added

- `AethexAI.list_tag_vocabulary()` / `AsyncAethexAI.list_tag_vocabulary()` — wrapper for `GET /api/v1/voices/tag-vocabulary`. Returns the closed-vocabulary tag set (tone, voice_texture, delivery_style, business_persona) used by voice tagging and accepted by `GET /voices?tag=...`.

### Changed

- `cancel_transcription_job` (sync and async) now returns a typed `CancelTranscriptionJobResponse` (`id`, `status`) instead of a raw `dict`, matching the other transcription wrappers. The on-the-wire shape is unchanged, but code that indexed the old dict result (e.g. `result["id"]`) must now use attribute access (`result.id`).
- **Breaking:** `list_agents`, `list_calls`, and `list_conversations` now return a `PaginatedResponse[T]` whose `.data` items are typed model instances (`AgentResponse`, `CallResponse`, `ConversationResponse` respectively) instead of raw dicts. Code that indexed items as dicts (e.g. `result.data[0]["id"]`) must be updated to use attribute access (`result.data[0].id`).
- The three list wrappers in `AethexAI`, `AsyncAethexAI`, and `Kora` now declare `-> PaginatedResponse[T]` return types (e.g. `PaginatedResponse[AgentResponse]`) so IDEs and mypy resolve the item type statically.
- `PaginatedResponse` now exposes a `has_more` property (`True` when `offset + len(data) < total`) for paging through multi-page result sets, and supports integer indexing (`page[0]` indexes into `.data`). The previous `__iter__` / `__len__` were removed because they silently operated on a single page — iterate `page.data` and loop while `page.has_more` to consume every page.
- `create_agent`, `update_agent`, and `duplicate_agent` now return a typed `AgentResponse` instead of a raw `dict`, so code can use attribute access (`agent.id`) instead of `agent["id"]`. The typed parsing is durable across SDK regenerations, including `update_agent` (PATCH 200).

### Fixed
- `send_offer()` / `send_ice_candidate()` no longer raise a false `Missing required field` error. `build_body` compared required fields by the generated Python attribute name (`type_`) instead of the JSON wire name (`type`), so the WebRTC signalling wrappers always rejected valid input before the request went out.
- `[realtime]` extra now installs from a binary wheel on supported Pythons instead of forcing a from-source PyAV build. Pinned to `av>=14.0.0,!=14.4.0,<15` so it resolves to `av==14.2.0` — the newest 14.x with cp310–cp313 wheels (FFmpeg bundled) — so no system FFmpeg is needed on manylinux, macOS, or Windows. (Alpine/musl has no `av` 14.x musllinux wheel and still builds from source.)
- Removed the public `get_conversation_diagnostics` wrapper from `AethexAI` / `AsyncAethexAI`. The endpoint is not callable with a public API key, so the wrapper is removed rather than repointed.
- Binary audio endpoints no longer crash with `UnicodeDecodeError` on success. `synthesize_speech`, `preview_voice`, and `stream_audio` / `get_conversation_audio` return `audio/wav`, but the spec typed the 200 response as `application/json`, so the generated client eagerly called `response.json()` on the WAV bytes. These methods now return raw `bytes` across `AethexAI`, `AsyncAethexAI`, and `Kora`.
- Resource-creation POSTs that return HTTP `201 Created` are parsed correctly instead of silently returning `None`. The generated success parse now accepts any 2xx status, so create wrappers (`create_agent`, `duplicate_agent`, `add_agent_tool`, `batch_synthesize`, `conversation_connect` behind `Conversation.start()`, and the rest) return the created resource whether the backend answers `200` or `201`; a no-content `204` returns `None` rather than crashing.
- `DeveloperClient.select_plan()` / `AsyncDeveloperClient.select_plan()` no longer raise `TypeError: Object of type Unset is not JSON serializable` when called without a body. `body` now defaults to `None`, so `select_plan("pro")` issues the POST with no JSON body and the server defaults to monthly billing. Pass a `SelectPlanRequest` to choose a different interval.
- Missing required body fields on POST wrappers (e.g. `create_agent`, `presign_upload`, `trigger_call`) now raise a typed `aethexai.ValidationError` listing every missing field, instead of a stdlib `KeyError` reporting only the first one. The request short-circuits before the wire call, and the error mirrors the server's 422 shape so callers can handle SDK pre-flight and server-side validation errors with one handler.
- 422 responses with the unified error envelope now raise the documented `aethexai.ValidationError` instead of crashing inside the generated parser. The FastAPI-shaped `detail: list[ValidationError]` shape continues to parse.
- `AethexAI.list_voices`, `AsyncAethexAI.list_voices`, and `Kora.list_voices` now forward the `tag` query parameter (and `supports_dialect_style` for `Kora.list_voices`), which were silently dropped by the wrappers.
- Method docstrings now link to the correct docs domain (`https://developers.aethexai.com/docs/...`). API methods point at `/docs/api-reference/<section>`; knowledge-base, webhook-trigger, and API-key/auth methods point at their `/docs/concepts/*` and `/docs/authentication` pages.

### Security & packaging
- The published package is strictly customer-facing. Internal and operational endpoints and internal-only surfaces are excluded from the bundled `openapi.json` and the generated client, and internal commentary is scrubbed from every shipped docstring. The source distribution ships only the package, `openapi.json`, `README`, `LICENSE`, and `CHANGELOG`.

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
