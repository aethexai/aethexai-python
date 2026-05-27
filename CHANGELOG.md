# Changelog

All notable changes to this project are documented here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `AethexAI.list_tag_vocabulary()` / `AsyncAethexAI.list_tag_vocabulary()` — wrapper for `GET /api/v1/voices/tag-vocabulary`. Returns the closed-vocabulary tag set (tone, voice_texture, delivery_style, business_persona) used by voice tagging and accepted by `GET /voices?tag=...`. (AET-1533)

### Changed

- `cancel_transcription_job` (sync and async) now returns a typed `CancelTranscriptionJobResponse` (`id`, `status`) instead of a raw `dict`, matching the other transcription wrappers. The on-the-wire shape is unchanged, but code that indexed the old dict result (e.g. `result["id"]`) must now use attribute access (`result.id`). (AET-1538)

### Fixed
- Removed the public `get_conversation_diagnostics` wrapper from `AethexAI` / `AsyncAethexAI`. The endpoint moved to an internal-only surface (shared-secret auth) in AET-1532, so the prod-openapi-sync relocated its generated op under `_generated/api/internal/` — leaving the public wrapper importing a path that no longer exists (broke `mypy`). The endpoint is not callable with a public API key, so the wrapper is removed rather than repointed. (AET-1532)

- Resource-creation POSTs that now return HTTP `201 Created` (backend AET-1566) are parsed correctly instead of silently returning `None`. The generated `_parse_response` branched only on `200`; on `201` it fell through to `return None`, and `_call` (which returns `response.parsed` for any 2xx) handed callers `None`, dropping the created resource. This broke `conversation_connect` (behind `Conversation.start()`), `create_agent`, `duplicate_agent`, `add_agent_tool`, `batch_synthesize`, and the other create wrappers. The affected `openapi.json` routes now declare `201`, and a post-codegen patch in `scripts/sync_from_prod.py` re-adds the `201` branch after every regeneration so the fix survives the next prod-spec sync. (AET-1580)
- `DeveloperClient.select_plan()` / `AsyncDeveloperClient.select_plan()` no longer raise `TypeError: Object of type Unset is not JSON serializable` when called without a body. The body is optional (the plan `slug` path param is the only required input), so `body` now defaults to `None` — the natural `select_plan("pro")` call issues the POST with no JSON body and the server defaults to monthly billing. Pass a `SelectPlanRequest` to choose a different interval. (AET-1581)
- Missing required body fields on POST wrappers (e.g. `create_agent`, `presign_upload`, `trigger_call`) now raise a typed `aethexai.ValidationError` listing every missing field, instead of a stdlib `KeyError` reporting only the first one. The request still short-circuits before the wire call. The error envelope mirrors the server's 422 shape (`code="validation_error"`, `detail=[{type,loc,msg,input}, ...]`, `fields` mirroring `detail`) so callers can write a single handler covering both SDK pre-flight and server-side validation errors. (AET-1524)
- 422 responses with the aethex unified error envelope (`{error, code, detail: <string>, request_id}`) now raise the documented `aethexai.ValidationError` instead of crashing inside the generated `HTTPValidationError.from_dict` with `ValueError: dictionary update sequence element #0 has length 1; 2 is required`. The FastAPI-shaped `detail: list[ValidationError]` shape continues to parse. (AET-1523)
- `AethexAI.list_voices`, `AsyncAethexAI.list_voices`, and `Kora.list_voices` now forward the OpenAPI `tag` query parameter (and `supports_dialect_style` for `Kora.list_voices`), which were silently dropped by the wrappers. (AET-1534)
- Method docstrings now link to the correct docs domain (`https://developers.aethexai.com/docs/...`) instead of the non-existent `docs.aethexai.com`. 79 links across `client.py` and `developer.py` were corrected: API methods point at `/docs/api-reference/<section>`, while knowledge-base, webhook-trigger, and API-key/auth methods point at their `/docs/concepts/*` and `/docs/authentication` pages. (AET-1578)

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
