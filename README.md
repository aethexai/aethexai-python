<div align="center">

# Aethex AI Python SDK

Deploy production voice agents with the AethexAI Voice API.

Create governed voice agents, place customer calls, synthesize speech,
transcribe recordings, and operate realtime voice workflows from Python.

[![PyPI version](https://img.shields.io/pypi/v/aethexai.svg)](https://pypi.org/project/aethexai/)
[![Python](https://img.shields.io/pypi/pyversions/aethexai.svg)](https://pypi.org/project/aethexai/)
[![CI](https://github.com/aethexai/aethexai-python/actions/workflows/test.yml/badge.svg)](https://github.com/aethexai/aethexai-python/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[Documentation](https://developers.aethexai.com/docs) ·
[Dashboard](https://developers.aethexai.com/dashboard) ·
[API Reference](https://developers.aethexai.com/docs/api-reference) ·
[Support](mailto:developers@aethexai.com)

</div>

## Install

```bash
pip install aethexai
```

Optional extras:

```bash
pip install "aethexai[realtime]"   # WebRTC conversations (Conversation class)
```

The `[realtime]` extra installs `aiortc` and `av` (PyAV). PyAV ships prebuilt
binary wheels (with FFmpeg bundled) for Linux, macOS, and Windows on Python
3.10–3.13, so a normal install needs **no** system FFmpeg. You only need system
FFmpeg if PyAV has to build from source (e.g. an unusual platform/arch): on
Debian/Ubuntu `apt install libavformat-dev libavfilter-dev libavdevice-dev`;
on macOS the pinned PyAV (14.x) targets FFmpeg 7, so install `brew install
ffmpeg@7` (plain `brew install ffmpeg` now gives FFmpeg 8, which this PyAV
release does not compile against).

Requires Python 3.10+.

## Quickstart

Create an agent for a customer operations workflow and place an outbound call.

```python
from aethexai import AethexAI

client = AethexAI(api_key="ae_live_...")  # or set AETHEX_API_KEY

voices = client.list_voices(language="french", limit=5)
voice = voices[0]

agent = client.create_agent(
    name="Customer Operations Assistant",
    system_prompt=(
        "You are a professional customer operations assistant. "
        "Help callers confirm appointments, answer policy questions, "
        "and escalate to a human when required."
    ),
    first_message="Bonjour, comment puis-je vous aider?",
    voice_id=voice.id,
    language="french",
    dialect_style="local",
)

call = client.trigger_call(
    agent_id=agent.id,
    to_number="+221700000000",
)

print(call.id, call.status)
```

## Clients

The SDK exposes two main clients.

| Client | Use it for |
|---|---|
| `AethexAI` | API-key authenticated platform operations: agents, calls, TTS, transcription jobs, conversations, phone numbers, SIP trunks, Twilio accounts, usage, uploads, and API keys. |
| `Kora` | Focused voice-agent workflows: agents, outbound calls, voices, TTS, transcription, and conversation history. |
| `DeveloperClient` | JWT-authenticated developer account and billing operations. |

Async code uses `AsyncAethexAI`, which mirrors the sync client method-for-method.

```python
import asyncio
from aethexai import AsyncAethexAI

async def main() -> None:
    async with AsyncAethexAI(api_key="ae_live_...") as client:
        voices = await client.list_voices(language="english")
        print([voice.id for voice in voices])

asyncio.run(main())
```

## Core Workflows

### Text to speech

Generate a complete audio asset for IVR, onboarding, or customer support:

```python
audio = client.synthesize_speech(
    text="Your appointment has been confirmed for tomorrow at 10 AM.",
    voice_id="fatima",
    language="english",
)

with open("appointment-confirmation.wav", "wb") as f:
    f.write(audio)
```

Stream audio chunks for low-latency playback:

```python
for chunk in client.stream_speech(
    text="I am checking your account now. Please hold for a moment.",
    voice_id="fatima",
    language="english",
):
    speaker.write(chunk)  # PCM16 audio chunks
```

### Transcription

For file transcription workflows, use `Kora`.

```python
from aethexai import Kora

kora = Kora("https://api.aethexai.com", "ae_live_...")

with open("call.wav", "rb") as f:
    result = kora.transcribe(
        f,
        language="french",
        file_name="call.wav",
        mime_type="audio/wav",
    )

print(result.text)
```

Submit longer recordings as asynchronous transcription jobs:

```python
import time
from aethexai import Kora

kora = Kora("https://api.aethexai.com", "ae_live_...")

with open("long-call.wav", "rb") as f:
    job = kora.transcribe_async(
        f,
        language="french",
        file_name="long-call.wav",
        mime_type="audio/wav",
    )

while True:
    job = kora.get_transcribe_job(job.id)
    if job.status in ("completed", "failed"):
        break
    time.sleep(2)

print(job.text)
```

### Realtime conversations

Install the realtime extra for full-duplex WebRTC conversations.

```bash
pip install "aethexai[realtime]"
```

```python
import asyncio
from aethexai import AsyncAethexAI
from aethexai.realtime import Conversation, ConversationCallbacks

async def main() -> None:
    client = AsyncAethexAI(api_key="ae_live_...")

    conversation = Conversation(
        client,
        agent_id="agent-uuid",
        callbacks=ConversationCallbacks(
            on_agent_text=lambda text: print("agent:", text),
            on_user_transcript=lambda text: print("user:", text),
        ),
    )

    await conversation.start()
    # Audio flows over WebRTC until you end the session.
    await conversation.end()
    await client.close()

asyncio.run(main())
```

## Platform Coverage

`AethexAI` uses a flat method surface: one method per endpoint, no nested
namespaces. This keeps platform automation explicit and easy to audit.

| Area | Methods |
|---|---|
| Agents | `create_agent`, `list_agents`, `get_agent`, `update_agent`, `delete_agent`, `duplicate_agent` |
| Tools | `add_agent_tool`, `list_agent_tools`, `update_agent_tool`, `delete_agent_tool` |
| Knowledge base | `upload_knowledge_doc`, `upload_knowledge_doc_by_upload`, `list_knowledge_docs`, `query_knowledge_base` |
| Calls | `trigger_call`, `batch_calls`, `list_calls`, `get_call`, `get_call_status` |
| TTS | `synthesize_speech`, `stream_speech`, `batch_synthesize`, `get_tts_batch` |
| Transcription | `transcribe_audio`, `transcribe_audio_async`, `get_transcription_job`, `cancel_transcription_job` |
| Conversations | `list_conversations`, `get_conversation`, `get_transcript`, `stream_audio`, `submit_feedback` |
| Phone and SIP | `list_phone_numbers`, `register_twilio_phone_number`, `register_sip_phone_number`, `list_sip_trunks` |
| Twilio accounts | `register_twilio_account`, `list_twilio_accounts`, `get_twilio_account`, `release_twilio_account` |
| Usage | `get_usage`, `get_usage_summary` |
| API keys | `list_api_keys`, `create_api_key`, `rotate_api_key`, `revoke_api_key` |

See the [API reference](https://developers.aethexai.com/docs/api-reference) for
request and response fields.

## Developer Account and Billing

Billing and account endpoints require a developer JWT from the dashboard auth
flow, not an API key. Use `DeveloperClient` for those calls.

```python
from aethexai import DeveloperClient

developer = DeveloperClient(
    access_token="eyJhbGciOi...",
    refresh_token="eyJhbGciOi...",  # optional; enables one retry after refresh
)

balance = developer.get_balance()
plans = developer.list_plans()
```

`DeveloperClient` reads `AETHEX_DEVELOPER_ACCESS_TOKEN` and
`AETHEX_DEVELOPER_REFRESH_TOKEN` when tokens are not passed explicitly.

## Configuration

```python
from aethexai import AethexAI

client = AethexAI(
    api_key="ae_live_...",
    base_url="https://api.aethexai.com",
    timeout=30.0,
    max_retries=2,
)
```

| Parameter | Default | Description |
|---|---|---|
| `api_key` | `$AETHEX_API_KEY` | API key sent as `X-API-Key`. |
| `base_url` | `https://api.aethexai.com` | AethexAI API base URL. |
| `timeout` | `30.0` | Per-request timeout in seconds. |
| `max_retries` | `2` | HTTP transport retries for retryable failures. |
| `httpx_client` | `None` | Optional custom `httpx.Client` or `httpx.AsyncClient`. |

## Errors

Non-2xx responses raise typed exceptions. Transport failures are mapped to SDK
errors, so production callers can centralize retry, alerting, and escalation
logic.

```python
from aethexai import (
    AethexAI,
    AethexError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

client = AethexAI(api_key="ae_live_...")

try:
    agent = client.get_agent("00000000-0000-0000-0000-000000000000")
except NotFoundError:
    print("Agent not found")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except AuthenticationError:
    print("Invalid API key")
except ValidationError as e:
    print(f"Request rejected: {e.response}")
except AethexError as e:
    print(f"SDK error: {e}")
```

| Status | Exception |
|---|---|
| 401 | `AuthenticationError` |
| 403 | `PermissionDeniedError` |
| 404 | `NotFoundError` |
| 409 | `ConflictError` |
| 422 | `ValidationError` |
| 429 | `RateLimitError` |
| 5xx | `InternalServerError` |
| Network failure | `APIConnectionError` |
| Timeout | `APITimeoutError` |

## Development

The generated REST client lives under `src/aethexai/_generated/` and is built
from `openapi.json`. The maintained SDK surface lives in:

- `src/aethexai/client.py`
- `src/aethexai/_async_client.py`
- `src/aethexai/kora.py`
- `src/aethexai/realtime/`

Run the local checks:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check src/ tests/ scripts/
uv run mypy src/aethexai
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full development workflow.

Questions about the SDK can be sent to
[developers@aethexai.com](mailto:developers@aethexai.com).

## Community

- GitHub: [github.com/Aethex-AI](https://github.com/Aethex-AI)
- X: [@aethexailabs](https://x.com/aethexailabs)
- LinkedIn: [AethexAI](https://www.linkedin.com/company/www.aethexai.com/)
- Discord: [discord.gg/3yAMnpRd](https://discord.gg/3yAMnpRd)

## License

Released under the [MIT License](LICENSE).
