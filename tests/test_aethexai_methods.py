"""End-to-end wrapper tests for representative ``AethexAI`` methods.

Each test uses ``respx`` to mock the underlying ``httpx`` transport, then
verifies the wrapper:

  1. issues the correct HTTP method and URL path
  2. serializes its request body as expected
  3. forwards path / query parameters correctly
  4. parses the response back to the expected Python value

We do not test all 96 methods exhaustively — we pick ~12 that span the major
verb / payload shapes (GET-list, GET-by-id, POST-body, PATCH, DELETE,
multi-arg path, binary response, paginated list).
"""

from __future__ import annotations

from uuid import uuid4

import httpx
import pytest
import respx

from aethexai import AethexAI

BASE_URL = "https://api.test.aethexai.com"


@pytest.fixture
def client() -> AethexAI:
    """A live ``AethexAI`` against a fake base_url; respx intercepts the wire."""
    c = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    yield c
    c.close()


# ─── voices ─────────────────────────────────────────────────────────────────


@respx.mock
def test_list_voices_get_voices(client: AethexAI) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/voices").mock(
        return_value=httpx.Response(
            200,
            json=[
                {"id": "fatima", "name": "Fatima", "language": "french"},
                {"id": "amir", "name": "Amir", "language": "arabic"},
            ],
        )
    )

    voices = client.list_voices()

    assert route.called
    req = route.calls.last.request
    assert req.method == "GET"
    assert req.url.path == "/api/v1/voices"
    # x-api-key header is set by the underlying authenticated client
    assert req.headers.get("x-api-key") == "ak_live_test"

    assert isinstance(voices, list)
    assert len(voices) == 2
    assert voices[0].id == "fatima"
    assert voices[1].id == "amir"


@respx.mock
def test_list_voices_forwards_query_params(client: AethexAI) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/voices").mock(return_value=httpx.Response(200, json=[]))

    client.list_voices(language="french", tag="warm", limit=10, offset=5)

    req = route.calls.last.request
    # respx exposes the query string as `params`
    qs = dict(req.url.params)
    assert qs.get("language") == "french"
    assert qs.get("tag") == "warm"
    assert qs.get("limit") == "10"
    assert qs.get("offset") == "5"


@respx.mock
def test_get_voice_uses_path_param(client: AethexAI) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/voices/fatima").mock(
        return_value=httpx.Response(
            200, json={"id": "fatima", "name": "Fatima", "language": "french"}
        )
    )

    voice = client.get_voice("fatima")

    assert route.called
    req = route.calls.last.request
    assert req.method == "GET"
    assert req.url.path == "/api/v1/voices/fatima"
    assert voice.id == "fatima"


# AET-1522: preview_voice and stream_audio return ``audio/wav`` bytes even
# though ``openapi.json`` declares ``application/json``. The wrappers must
# bypass the generated JSON parser and return raw bytes. We use a binary
# payload (non-UTF-8 leading bytes) so a regression would surface as a
# ``UnicodeDecodeError`` rather than silently being swallowed by a payload
# that happens to be valid ASCII.
_WAV_PAYLOAD = b"RIFF\x24\x00\x00\x00WAVE\xc0\x92\xbabinaryaudiopayload"


@respx.mock
def test_preview_voice_returns_audio_bytes(client: AethexAI) -> None:
    route = respx.post(f"{BASE_URL}/api/v1/voices/preview").mock(
        return_value=httpx.Response(
            200, content=_WAV_PAYLOAD, headers={"content-type": "audio/wav"}
        )
    )

    audio = client.preview_voice(voice_id="fatima", text="Hello.")

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == "/api/v1/voices/preview"
    import json as _json

    sent = _json.loads(req.content.decode())
    assert sent["voice_id"] == "fatima"
    assert sent["text"] == "Hello."
    assert isinstance(audio, bytes)
    assert audio == _WAV_PAYLOAD


@respx.mock
def test_stream_audio_returns_audio_bytes(client: AethexAI) -> None:
    conv_id = uuid4()
    route = respx.get(f"{BASE_URL}/api/v1/conversations/{conv_id}/audio.wav").mock(
        return_value=httpx.Response(
            200, content=_WAV_PAYLOAD, headers={"content-type": "audio/wav"}
        )
    )

    audio = client.stream_audio(conv_id, token="t-abc", range_="bytes=0-1023")

    assert route.called
    req = route.calls.last.request
    assert req.method == "GET"
    assert req.url.path == f"/api/v1/conversations/{conv_id}/audio.wav"
    assert dict(req.url.params).get("token") == "t-abc"
    assert req.headers.get("range") == "bytes=0-1023"
    assert isinstance(audio, bytes)
    assert audio == _WAV_PAYLOAD


@respx.mock
def test_list_tag_vocabulary_returns_typed_model(client: AethexAI) -> None:
    payload = {
        "tone": ["warm", "calm"],
        "voice_texture": ["smooth", "deep"],
        "delivery_style": ["natural", "expressive"],
        "business_persona": ["professional", "trustworthy"],
    }
    route = respx.get(f"{BASE_URL}/api/v1/voices/tag-vocabulary").mock(
        return_value=httpx.Response(200, json=payload)
    )

    vocab = client.list_tag_vocabulary()

    assert route.called
    req = route.calls.last.request
    assert req.method == "GET"
    assert req.url.path == "/api/v1/voices/tag-vocabulary"

    # Returns a typed model (not a raw dict) — exercise its to_dict round-trip.
    assert not isinstance(vocab, dict)
    assert hasattr(vocab, "to_dict")
    assert vocab.to_dict() == payload


# ─── agents ─────────────────────────────────────────────────────────────────


@respx.mock
def test_list_agents(client: AethexAI) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": str(uuid4()), "name": "Agent A"}],
                "total": 1,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    client.list_agents()

    assert route.called
    req = route.calls.last.request
    assert req.method == "GET"
    assert req.url.path == "/api/v1/agents"


@respx.mock
def test_create_agent_sends_json_body(client: AethexAI) -> None:
    route = respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(200, json={"id": "agent-1", "name": "Bot"})
    )

    client.create_agent(
        name="Bot",
        system_prompt="You are helpful.",
        voice_id="fatima",
    )

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == "/api/v1/agents"
    assert req.headers.get("content-type") == "application/json"

    import json

    body = json.loads(req.content.decode())
    assert body["name"] == "Bot"
    assert body["system_prompt"] == "You are helpful."
    assert body["voice_id"] == "fatima"


@respx.mock
def test_get_agent_quotes_uuid_in_path(client: AethexAI) -> None:
    agent_uuid = uuid4()
    route = respx.get(f"{BASE_URL}/api/v1/agents/{agent_uuid}").mock(
        return_value=httpx.Response(200, json={"id": str(agent_uuid), "name": "Agent"})
    )

    agent = client.get_agent(agent_uuid)

    assert route.called
    req = route.calls.last.request
    assert req.url.path == f"/api/v1/agents/{agent_uuid}"
    assert agent.id == str(agent_uuid)


@respx.mock
def test_get_agent_accepts_string_uuid(client: AethexAI) -> None:
    agent_uuid = uuid4()
    route = respx.get(f"{BASE_URL}/api/v1/agents/{agent_uuid}").mock(
        return_value=httpx.Response(200, json={"id": str(agent_uuid), "name": "X"})
    )

    client.get_agent(str(agent_uuid))
    assert route.called


@respx.mock
def test_update_agent_uses_patch(client: AethexAI) -> None:
    agent_uuid = uuid4()
    route = respx.patch(f"{BASE_URL}/api/v1/agents/{agent_uuid}").mock(
        return_value=httpx.Response(200, json={"id": str(agent_uuid), "name": "Updated"})
    )

    client.update_agent(agent_uuid, name="Updated")

    assert route.called
    req = route.calls.last.request
    assert req.method == "PATCH"
    import json

    body = json.loads(req.content.decode())
    assert body["name"] == "Updated"


@respx.mock
def test_delete_agent_uses_delete(client: AethexAI) -> None:
    agent_uuid = uuid4()
    route = respx.delete(f"{BASE_URL}/api/v1/agents/{agent_uuid}").mock(
        # delete typically returns 204 with no content
        return_value=httpx.Response(204, content=b"")
    )

    result = client.delete_agent(agent_uuid)

    assert route.called
    req = route.calls.last.request
    assert req.method == "DELETE"
    # parsed body is None on 204 (the generated client falls through to None)
    assert result is None


# ─── transcription ──────────────────────────────────────────────────────────


@respx.mock
def test_cancel_transcription_job_returns_typed_model(client: AethexAI) -> None:
    """AET-1538: DELETE /transcribe/{job_id} parses to ``CancelTranscriptionJobResponse``.

    Previously the route had an empty 200 response schema, so the generated
    parser returned a raw dict and the SDK wrapper exposed ``Any``. The
    backend now declares ``CancelTranscriptionJobResponse``; this pins that
    the wrapper returns the typed model (parity with ``get_transcription_job``).
    """
    from aethexai._generated.models.cancel_transcription_job_response import (
        CancelTranscriptionJobResponse,
    )

    job_uuid = uuid4()
    route = respx.delete(f"{BASE_URL}/api/v1/transcribe/{job_uuid}").mock(
        return_value=httpx.Response(200, json={"id": str(job_uuid), "status": "cancelled"})
    )

    result = client.cancel_transcription_job(job_uuid)

    assert route.called
    req = route.calls.last.request
    assert req.method == "DELETE"
    assert req.url.path == f"/api/v1/transcribe/{job_uuid}"
    assert isinstance(result, CancelTranscriptionJobResponse)
    assert result.id == str(job_uuid)
    assert result.status == "cancelled"


# ─── calls ──────────────────────────────────────────────────────────────────


@respx.mock
def test_trigger_call(client: AethexAI) -> None:
    agent_id = str(uuid4())
    route = respx.post(f"{BASE_URL}/api/v1/calls/trigger").mock(
        return_value=httpx.Response(202, json={"call_id": "call-1", "status": "queued"})
    )

    client.trigger_call(agent_id=agent_id, to_number="+221770000000")

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == "/api/v1/calls/trigger"
    import json

    body = json.loads(req.content.decode())
    assert body["agent_id"] == agent_id
    assert body["to_number"] == "+221770000000"


@respx.mock
def test_get_call_status(client: AethexAI) -> None:
    call_uuid = uuid4()
    route = respx.get(f"{BASE_URL}/api/v1/calls/{call_uuid}/status").mock(
        return_value=httpx.Response(
            200,
            json={
                "status": "in-progress",
                "provider": "twilio",
                "duration_s": 12.5,
            },
        )
    )

    client.get_call_status(call_uuid)

    assert route.called
    req = route.calls.last.request
    assert req.method == "GET"
    assert req.url.path == f"/api/v1/calls/{call_uuid}/status"


# ─── tts ────────────────────────────────────────────────────────────────────


@respx.mock
def test_synthesize_speech_posts_text_and_voice(client: AethexAI) -> None:
    audio_blob = b"WAVDATA"
    route = respx.post(f"{BASE_URL}/api/v1/tts").mock(
        return_value=httpx.Response(200, content=audio_blob, headers={"content-type": "audio/wav"})
    )

    audio = client.synthesize_speech(text="Hello", voice_id="fatima")

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == "/api/v1/tts"
    import json

    body = json.loads(req.content.decode())
    assert body["text"] == "Hello"
    assert body["voice_id"] == "fatima"
    assert audio == audio_blob


@respx.mock
def test_stream_speech_yields_chunks(client: AethexAI) -> None:
    audio_blob = b"ABCD" * 1024
    route = respx.post(f"{BASE_URL}/api/v1/tts/stream").mock(
        return_value=httpx.Response(200, content=audio_blob, headers={"content-type": "audio/wav"})
    )

    chunks = list(client.stream_speech(text="Hello", voice_id="fatima", chunk_size=512))

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == "/api/v1/tts/stream"
    assert b"".join(chunks) == audio_blob


# ─── usage ─────────────────────────────────────────────────────────────
#
# (Billing methods moved to ``DeveloperClient`` per audit A.1 —
# see ``tests/test_developer_client.py``.)


@respx.mock
def test_get_usage(client: AethexAI) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/usage").mock(
        return_value=httpx.Response(
            200,
            json={
                "period": "2025-05",
                "minutes_used": 42,
                "credits_used": 50,
            },
        )
    )

    client.get_usage()

    assert route.called
    req = route.calls.last.request
    assert req.method == "GET"
    assert req.url.path == "/api/v1/usage"


# ─── twilio accounts ────────────────────────────────────────────────────────


@respx.mock
def test_register_twilio_account(client: AethexAI) -> None:
    route = respx.post(f"{BASE_URL}/api/v1/twilio-accounts").mock(
        return_value=httpx.Response(
            201,
            json={
                "id": str(uuid4()),
                "account_sid": "AC0123456789abcdef0123456789abcdef",
                "friendly_name": "Production Twilio account",
                "status": "active",
                "tenant_id": str(uuid4()),
            },
        )
    )

    account = client.register_twilio_account(
        account_sid="AC0123456789abcdef0123456789abcdef",
        auth_token="secret",
        friendly_name="Production Twilio account",
    )

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == "/api/v1/twilio-accounts"
    import json

    body = json.loads(req.content.decode())
    assert body["account_sid"] == "AC0123456789abcdef0123456789abcdef"
    assert body["auth_token"] == "secret"
    assert account.status == "active"


# ─── api keys ───────────────────────────────────────────────────────────────


@respx.mock
def test_rotate_api_key(client: AethexAI) -> None:
    key_uuid = uuid4()
    route = respx.post(f"{BASE_URL}/api/v1/api-keys/{key_uuid}/rotate").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": str(key_uuid),
                "key_prefix": "ak_live_",
                "name": "default",
                "scopes": ["read", "write"],
                "rate_limit_rpm": 60,
                "rate_limit_daily": 1000,
                "key": "ak_live_new_secret",
            },
        )
    )

    client.rotate_api_key(key_uuid)

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == f"/api/v1/api-keys/{key_uuid}/rotate"


@respx.mock
def test_create_api_key(client: AethexAI) -> None:
    route = respx.post(f"{BASE_URL}/api/v1/api-keys").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "key-1",
                "key_prefix": "ak_live_",
                "name": "test",
                "scopes": ["read"],
                "rate_limit_rpm": 60,
                "rate_limit_daily": 1000,
                "key": "ak_live_x",
            },
        )
    )

    client.create_api_key(name="test")

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == "/api/v1/api-keys"
    import json

    body = json.loads(req.content.decode())
    assert body["name"] == "test"


# ─── models ─────────────────────────────────────────────────────────────────


@respx.mock
def test_list_models(client: AethexAI) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/models").mock(
        return_value=httpx.Response(
            200,
            json=[
                {"id": "gpt-4", "provider": "openai", "available": True},
                {"id": "claude-3", "provider": "anthropic", "available": True},
            ],
        )
    )

    client.list_models()

    assert route.called
    req = route.calls.last.request
    assert req.url.path == "/api/v1/models"


# ─── conversations ──────────────────────────────────────────────────────────


@respx.mock
def test_list_conversations(client: AethexAI) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/conversations").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": "c1", "agent_id": "a1"}],
                "total": 1,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    client.list_conversations(limit=25, offset=0)

    req = route.calls.last.request
    qs = dict(req.url.params)
    assert qs.get("limit") == "25"


@respx.mock
def test_get_transcript_path(client: AethexAI) -> None:
    conv_uuid = uuid4()
    route = respx.get(f"{BASE_URL}/api/v1/conversations/{conv_uuid}/transcript").mock(
        return_value=httpx.Response(
            200,
            json=[
                {"id": "turn-1", "turn_index": 0, "role": "user", "text": "Hi"},
                {"id": "turn-2", "turn_index": 1, "role": "assistant", "text": "Hello!"},
            ],
        )
    )

    client.get_transcript(conv_uuid)

    assert route.called
    req = route.calls.last.request
    assert req.url.path == f"/api/v1/conversations/{conv_uuid}/transcript"
