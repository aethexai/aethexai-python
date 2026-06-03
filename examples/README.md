# Aethex AI Python SDK — Examples

A small, self-contained tour of the SDK. Each script is runnable on its
own; together they cover the surface most apps use day-to-day: agent
creation, outbound calling, text-to-speech, transcription, and live
WebRTC conversations.

## Setup

```bash
# from the repo root
uv sync
export AETHEX_API_KEY=ae_live_...   # or ae_test_...
```

For the realtime example you also need the optional WebRTC extra:

```bash
uv pip install 'aethexai[realtime]'
```

## The examples

| File                                    | Client used      | What it shows                                                                                  | Needs an existing agent? |
| --------------------------------------- | ---------------- | ---------------------------------------------------------------------------------------------- | ------------------------ |
| `kora_quickstart.py`                    | `Kora`           | The 60-second "hello world": create an agent, place an outbound call.                          | No (creates one)         |
| `agent_create_and_call.py`              | `AethexAI`       | Full agent lifecycle: create, upload a knowledge-base doc, patch settings, call, poll status.  | No (creates one)         |
| `tts_streaming.py`                      | `AethexAI`       | TTS in both flavors: one-shot synthesis (JSON envelope -> file) and chunked PCM16 streaming.   | No                       |
| `transcribe_file.py`                    | `AethexAI`       | Sync transcription plus async submit-and-poll, with an optional `language` hint.               | No                       |
| `realtime_conversation.py`              | `AsyncAethexAI`  | WebRTC live conversation with audio/text callbacks, mid-call `send_text` and `inject_context`. | Yes (`AGENT_ID`)         |

## Running them

```bash
uv run python examples/kora_quickstart.py
uv run python examples/agent_create_and_call.py
uv run python examples/tts_streaming.py
uv run python examples/transcribe_file.py
uv run python examples/realtime_conversation.py
```

## Environment variables at a glance

| Variable                  | Used by                                              | Notes                                                          |
| ------------------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| `AETHEX_API_KEY`          | **all**                                              | Required everywhere.                                           |
| `AETHEX_BASE_URL`         | all                                                  | Override the default `https://api.aethexai.com`.               |
| `PHONE_NUMBER`            | `kora_quickstart`, `agent_create_and_call`           | E.164 destination, e.g. `+221700000000`.                       |
| `TTS_TEXT` / `TTS_VOICE_ID` / `TTS_LANGUAGE` / `OUT_DIR` | `tts_streaming`                          | Customize the synthesis input and output location.             |
| `AUDIO_FILE`              | `transcribe_file`                                    | Absolute path to a local audio file. **Required** for that script. |
| `TRANSCRIBE_LANGUAGE`     | `transcribe_file`                                    | Optional language hint (e.g. `en`, `fr`).                      |
| `AGENT_ID`                | `realtime_conversation`                              | Id of an existing agent. **Required** for that script.         |
| `CONV_DURATION_SECONDS` / `CONV_GREETING` | `realtime_conversation`              | Control how long the call runs and what text gets injected.    |
