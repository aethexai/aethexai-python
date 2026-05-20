# Changelog

All notable changes to this project are documented here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] — 2026-05-20

First public release on PyPI. Version 0.2.0 was uploaded earlier and immediately deleted due to incomplete state; PyPI policy reserves that version number permanently, so this release starts at 0.2.1.

### Added
- Full rebuild from OpenAPI spec — flat-method `AethexAI` and `AsyncAethexAI` (96 methods each), voice-focused `Kora` (22 methods)
- Sync mechanism: `scripts/dump_openapi.py` and `scripts/sync_from_prod.py` keep the SDK aligned with the production API
- Typed exception hierarchy with HTTP status mapping (`AuthenticationError`, `NotFoundError`, etc.)
- Real-time WebRTC `Conversation` (in `aethexai.realtime`)
- Unit test suite with `respx` HTTP mocks plus optional live-API integration tests
- **`DeveloperClient` / `AsyncDeveloperClient`** — JWT-authenticated client
  for billing and account endpoints (`/api/v1/billing/*`, `/api/v1/auth/me`).
  Carries `Authorization: Bearer <jwt>`; auto-refreshes on 401 via
  `POST /api/v1/auth/refresh` when a refresh token is provided.
  Tokens come from the magic-link / Google sign-in flow at
  `developers.aethexai.com`.

### Changed
- Resource classes (`client.agents.create(...)`) replaced by flat methods (`client.create_agent(...)`)
- Top-level convenience helpers `kora_speak()` / `kora_read()` removed — use `Kora(...)` instance methods instead
- `Conversation` now routes its three signaling calls through the public
  wrappers `AsyncAethexAI.conversation_connect()`, `.send_offer()`, and
  `.end_conversation_session()` — at the correct `/api/v1/conversation/...`
  paths. Previously the class targeted a non-existent
  `_client._client_wrapper` attribute and unprefixed `/conversation/*`
  paths; both failed dead-on-arrival.

### Removed
- Dead resource modules from earlier iterations: `campaigns`, `chat`, `insights`, `pronunciation`, `webhooks` (none matched a real endpoint)
- **8 billing methods on `AethexAI` / `AsyncAethexAI`** — `get_balance`,
  `list_plans`, `select_plan`, `list_invoices`, `list_transactions`,
  `list_payment_methods`, `create_payment_method_setup_intent`,
  `detach_payment_method`. The corresponding server routes require a
  developer JWT (`Authorization: Bearer …`), but `AethexAI` only sends
  `X-API-Key` — every call returned 401 against the live server. Use
  `aethexai.DeveloperClient` instead.
- `aethexai.realtime.TranscribeStream` — the server route `/ws/v1/transcribe`
  was removed and customer-facing streaming transcribe is deferred to v2.
  Use `client.transcribe_audio()` (sync) or `client.transcribe_audio_async()`
  (webhook) instead.
- `aethexai.realtime.VoiceStream` — the server route `/ws/v1/voice` was
  removed; a standalone full-agent WebSocket is deferred to v2. Use Twilio
  or WebRTC (`Conversation`) for voice agents.
- `[websocket]` optional dependency — no SDK consumer left after the
  TranscribeStream/VoiceStream removal.
- `Conversation.send_text()` and `Conversation.inject_context()` — neither
  has a backing server endpoint. For mid-conversation text, send on the
  open `chat` data channel (`conv._dc.send(...)`); for tool-call results
  use `AsyncAethexAI.send_tool_result()`.
- `AethexAI.get_conversation_signed_url()` and
  `AethexAI.get_conversation_token()` (plus their async equivalents).
  The backend routes `/api/v1/conversation/get-signed-url` and
  `/api/v1/conversation/token` were removed upstream; both wrappers would
  `ImportError` on the regenerated `_generated/api/conversation` module
  that no longer contains the underlying operations. Open WebRTC sessions
  via `conversation_connect()` from your server, which holds the API key
  and proxies `/connect`, `/offer`, and `/ice` for browser clients.

### Fixed
- `scripts/sync_from_prod.py`: the post-codegen secret-fields patch
  now matches the `from attrs import ...` anchor by line prefix
  instead of exact identifier order. `openapi-python-client` reorders
  those imports between releases; the old exact-string match silently
  skipped sentinel insertion when the order changed, which could leak
  the API key into `repr(client)`.

### Synced
- `openapi.json` and `src/aethexai/_generated/` regenerated against
  the latest backend OpenAPI spec. New backend surface picked up:
  `/api/v1/auth/logout-all`, `/api/v1/auth/sessions`, the
  `/api/v1/dashboard/*` endpoints, `/api/v1/voices/tag-vocabulary`,
  and `PATCH /internal/voices/{voice_key}`.
