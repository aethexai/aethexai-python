# Changelog

All notable changes to this project are documented here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- New optional `audio` extra (`pip install "aethexai[audio]"`) installs PyAV (`av`) for client-side audio format conversion / normalization in transcription. With it installed, the sync transcription paths decode any input (mp3, m4a, stereo or 48kHz WAV, etc.) to canonical 24kHz mono 16-bit PCM WAV before chunking; without it the paths fall back to WAV-only handling and send non-canonical input as-is. Same `av` pin as the `realtime` extra, so it resolves to a binary wheel with no system FFmpeg required on supported platforms.

### Changed

- **Unknown keyword arguments to `**fields` create/update wrappers are now rejected** with a typed `aethexai.ValidationError` that names the offending key, instead of being silently absorbed into `additional_properties` (where the server ignored them, so a typo'd field name silently did nothing). `create_agent` and `update_agent` (on both `AethexAI`/`AsyncAethexAI` and `Kora`) are the deliberate exception — they continue to tolerate and forward extra fields, because extra-kwarg passthrough was already part of their documented contract (so rejecting it would be a behavior regression). The other wrappers never promised field-passthrough, so there a clear typo error is the better default.
- `send_ice_candidate()` (sync and async) now documents that the request body takes a `candidates` **list** plus a `pc_id`, not a singular `candidate` — the method name is singular but the wire contract is plural. Passing `candidate=` raises `ValidationError` naming the required `candidates` / `pc_id` fields. The wire contract is unchanged.

### Fixed

- Invalid input now raises a typed `aethexai.ValidationError` *before the request goes out*, instead of a stdlib `ValueError`/`TypeError` that escaped `except aethexai.AethexError`:
  - **Malformed path-parameter UUIDs** — `get_agent("bad-uuid")`, `get_call(...)`, and every other id-by-path method across `AethexAI`, `AsyncAethexAI`, and `Kora` now raise `ValidationError` (422, `code="validation_error"`) naming the path field.
  - **Malformed request bodies** that previously failed deep inside the generated `from_dict` — wrong nested shapes (`batch_calls(recipients=["+1555..."])`), body UUIDs (`conversation_connect(agent_id="bad-uuid")`), and wrong container types (`batch_synthesize(items="notalist")`) — now surface as `ValidationError`.
  - `Kora.create_agent` / `Kora.update_agent` no longer raise a raw `TypeError` on an unknown keyword argument; they route through the same `build_body` path as `AethexAI` and forward extras for parity.
- A **whitespace-only `api_key`** is now rejected at construction like an empty one: `AethexAI` / `AsyncAethexAI` raise `AuthenticationError` (401) and `Kora` raises `ValueError`, instead of constructing successfully and later failing with an opaque `APIConnectionError`.
- Constructing a client without an API key (`AethexAI(api_key="")` / `AsyncAethexAI()` with no `AETHEX_API_KEY`) now raises `AuthenticationError` with `code="authentication_error"` instead of the mislabeled `code="internal_error"`. The `status_code` was already `401`; only the `code` was wrong, and it now matches the slug the server returns for a 401 so a single error handler keyed on `code` works for both.
- `upload_knowledge_doc` (sync and async) now accepts friendly keyword arguments — `text=`, `file=` (raw `bytes`, a binary stream, or a `File`), `filename=`, plus `file_name=` / `mime_type=` for the uploaded part — and builds the multipart request internally. Previously the only working call required passing a pre-built internal request model, so the intuitive `upload_knowledge_doc(agent_id, text="...")` raised `AttributeError`. Calling it with neither `text` nor `file` now raises a typed `aethexai.ValidationError` before the request goes out. Passing a pre-built `body=` is still supported and takes precedence.
- `Kora.transcribe`, `AethexAI.transcribe_audio`, and `AsyncAethexAI.transcribe_audio` now transcribe recordings longer than 35s. Audio passed as `bytes`, a stream, or a `File` is normalized to canonical 24kHz mono 16-bit WAV (via the optional `audio` extra; WAV-only fallback otherwise) and split on silence at ≤30s boundaries — a margin under the ~35s per-request cap that avoids cutting words mid-syllable — then transcribed per chunk and concatenated as space-joined text. The merge is text-based because the backend returns no segments (chunks are contiguous and non-overlapping, so no seam de-duplication is needed). The async-job / by-upload paths are unchanged.
- The inline async transcription routes (`transcribe_async`, `transcribe_audio_async`) now raise a typed `aethexai.ValidationError` client-side when handed a WAV longer than the ~35s per-request limit, pointing callers at the auto-chunking `Kora.transcribe` / `AethexAI.transcribe_audio` paths instead of failing with the opaque server "Audio too long" error. The by-upload routes only receive an `upload_id` (no local bytes) and remain server-bound.
- `PaginatedResponse` now implements a consistent sequence protocol over `.data`. `len(page)` works (previously raised `TypeError: object of type 'PaginatedResponse' has no len()`); `len`, integer/slice indexing, iteration, `in`, and `del` all operate on the page's items. Previously the protocol was mixed — `page[0]` returned a typed item while `x in page` and `del page[...]` silently targeted `additional_properties`. Note that `x in page` now tests membership against the page items (`.data`) rather than `additional_properties` keys. Forward-compat extra fields remain reachable via the `additional_properties` attribute, `additional_keys`, and string-key subscript (`page["key"]` / `page["key"] = ...`). Each `PaginatedResponse` still holds one page — loop while `page.has_more` to consume every page.

## [0.4.0] — 2026-06-02

Synced to the current backend OpenAPI contract and adds a voice-catalog helper.

### Added

- `AethexAI.list_countries()` / `AsyncAethexAI.list_countries()` — wrapper for `GET /api/v1/voices/countries`. Returns the closed set of ISO 3166-1 alpha-2 country codes (as `{"code", "name"}` items) accepted by the `country` filter on `list_voices`, so a country picker can be rendered without hardcoding the list.
- `AethexAI.list_tag_vocabulary()` / `AsyncAethexAI.list_tag_vocabulary()` — wrapper for `GET /api/v1/voices/tag-vocabulary`. Returns the closed-vocabulary tag set (tone, voice_texture, delivery_style, business_persona) used by voice tagging and accepted by `GET /voices?tag=...`.

### Changed

- `cancel_transcription_job` (sync and async) now returns a typed `CancelTranscriptionJobResponse` (`id`, `status`) instead of a raw `dict`, matching the other transcription wrappers. The on-the-wire shape is unchanged, but code that indexed the old dict result (e.g. `result["id"]`) must now use attribute access (`result.id`).
- **Breaking:** `list_agents`, `list_calls`, and `list_conversations` now return a `PaginatedResponse[T]` whose `.data` items are typed model instances (`AgentResponse`, `CallResponse`, `ConversationResponse` respectively) instead of raw dicts. Code that indexed items as dicts (e.g. `result.data[0]["id"]`) must be updated to use attribute access (`result.data[0].id`).
- The three list wrappers in `AethexAI`, `AsyncAethexAI`, and `Kora` now declare `-> PaginatedResponse[T]` return types (e.g. `PaginatedResponse[AgentResponse]`) so IDEs and mypy resolve the item type statically.
- `PaginatedResponse` now exposes a `has_more` property (`True` when `offset + len(data) < total`) for paging through multi-page result sets, and supports integer indexing (`page[0]` indexes into `.data`). The previous `__iter__` / `__len__` were removed because they silently operated on a single page — iterate `page.data` and loop while `page.has_more` to consume every page.
- `create_agent`, `update_agent`, and `duplicate_agent` now return a typed `AgentResponse` instead of a raw `dict`, so code can use attribute access (`agent.id`) instead of `agent["id"]`. The typed parsing is durable across SDK regenerations, including `update_agent` (PATCH 200).

### Fixed
- `Kora.transcribe` now transcribes WAV recordings longer than 35s. When WAV audio is passed as `bytes` and exceeds 35s it is split into ≤35s chunks, transcribed per chunk, and the transcripts are concatenated (`.segments` reflect only the first chunk). Non-WAV bytes and stream/`File` inputs are unchanged.
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
