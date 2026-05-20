# Changelog

All notable changes to this project are documented here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
