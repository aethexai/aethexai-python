"""End-to-end wrapper tests for representative ``Kora`` methods.

Each test uses ``respx`` to intercept the underlying ``httpx`` transport
and verifies the wrapper:

  1. issues the correct HTTP verb and URL path
  2. serializes its body / multipart / query params correctly
  3. parses the response back to a sane Python value
  4. returns bytes for the binary endpoints (TTS, conversation audio)

We do not exhaustively cover every Kora method — we pick ~12 that span the
distinct payload / response shapes Kora exposes (JSON, multipart, binary,
streamed bytes).
"""

from __future__ import annotations

import json
from uuid import uuid4

import httpx
import pytest
import respx

from aethexai import Kora

BASE_URL = "https://api.test.aethexai.com"


@pytest.fixture
def kora() -> Kora:
    """A live ``Kora`` against a fake base_url; respx intercepts the wire."""
    k = Kora(BASE_URL, "ae_live_kora_test")
    yield k
    k.close()


# ─── construction sanity ────────────────────────────────────────────────────


def test_kora_positional_constructor_round_trip() -> None:
    k = Kora(BASE_URL, "ae_live_xyz")
    assert k._base_url == BASE_URL
    # x-api-key header must be wired on the underlying client. The raw key
    # is NOT stored on the Kora instance (see finding A.5 of the 2026-05-17
    # pre-launch audit) — the only authoritative location is the auth header
    # that goes out on every request.
    hc = k._client.get_httpx_client()
    assert hc.headers.get("x-api-key") == "ae_live_xyz"
    k.close()


# ─── voices ─────────────────────────────────────────────────────────────────


@respx.mock
def test_kora_list_voices(kora: Kora) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/voices").mock(
        return_value=httpx.Response(
            200,
            json=[
                {"id": "fatima", "name": "Fatima", "language": "french"},
                {"id": "amir", "name": "Amir", "language": "arabic"},
            ],
        )
    )

    voices = kora.list_voices()

    assert route.called
    req = route.calls.last.request
    assert req.method == "GET"
    assert req.url.path == "/api/v1/voices"
    assert req.headers.get("x-api-key") == "ae_live_kora_test"
    assert isinstance(voices, list)
    assert len(voices) == 2
    assert voices[0].id == "fatima"
    assert voices[1].id == "amir"


@respx.mock
def test_kora_list_voices_with_language_filter(kora: Kora) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/voices").mock(return_value=httpx.Response(200, json=[]))

    kora.list_voices(language="french", limit=5, offset=10)

    req = route.calls.last.request
    qs = dict(req.url.params)
    assert qs.get("language") == "french"
    assert qs.get("limit") == "5"
    assert qs.get("offset") == "10"


@respx.mock
def test_kora_list_voices_forwards_tag_param(kora: Kora) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/voices").mock(return_value=httpx.Response(200, json=[]))

    kora.list_voices(tag="warm", supports_dialect_style=True, limit=5, offset=10)

    req = route.calls.last.request
    qs = dict(req.url.params)
    assert qs.get("tag") == "warm"
    assert qs.get("supports_dialect_style") == "true"
    assert qs.get("limit") == "5"
    assert qs.get("offset") == "10"


@respx.mock
def test_kora_get_voice_path_param(kora: Kora) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/voices/fatima").mock(
        return_value=httpx.Response(
            200, json={"id": "fatima", "name": "Fatima", "language": "french"}
        )
    )

    voice = kora.get_voice("fatima")

    assert route.called
    assert route.calls.last.request.url.path == "/api/v1/voices/fatima"
    assert voice.id == "fatima"


# ─── agents ─────────────────────────────────────────────────────────────────


@respx.mock
def test_kora_create_agent_posts_json_body(kora: Kora) -> None:
    route = respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(200, json={"id": "ag-1", "name": "Banker"})
    )

    kora.create_agent(
        name="Banker",
        system_prompt="You handle account questions.",
        voice_id="fatima",
        language="french",
        dialect_style="local",
        first_message="Bonjour!",
    )

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == "/api/v1/agents"
    assert req.headers.get("content-type") == "application/json"
    body = json.loads(req.content.decode())
    assert body["name"] == "Banker"
    assert body["system_prompt"] == "You handle account questions."
    assert body["voice_id"] == "fatima"
    assert body["language"] == "french"
    assert body["dialect_style"] == "local"
    assert body["first_message"] == "Bonjour!"


@respx.mock
def test_kora_update_agent_patch(kora: Kora) -> None:
    agent_id = uuid4()
    route = respx.patch(f"{BASE_URL}/api/v1/agents/{agent_id}").mock(
        return_value=httpx.Response(200, json={"id": str(agent_id), "name": "New"})
    )

    kora.update_agent(agent_id, name="New", language="english")

    assert route.called
    req = route.calls.last.request
    assert req.method == "PATCH"
    body = json.loads(req.content.decode())
    assert body["name"] == "New"
    assert body["language"] == "english"


@respx.mock
def test_kora_delete_agent(kora: Kora) -> None:
    agent_id = uuid4()
    route = respx.delete(f"{BASE_URL}/api/v1/agents/{agent_id}").mock(
        return_value=httpx.Response(204, content=b"")
    )

    result = kora.delete_agent(agent_id)

    assert route.called
    assert route.calls.last.request.method == "DELETE"
    # 204 doesn't match the generated 200-branch, so parsed=None
    assert result is None


# ─── calls ──────────────────────────────────────────────────────────────────


@respx.mock
def test_kora_trigger_call(kora: Kora) -> None:
    agent_id = str(uuid4())
    route = respx.post(f"{BASE_URL}/api/v1/calls/trigger").mock(
        return_value=httpx.Response(202, json={"id": "call-1", "status": "queued"})
    )

    kora.trigger_call(agent_id, to_number="+221770000000", from_number="+221780000000")

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == "/api/v1/calls/trigger"
    body = json.loads(req.content.decode())
    assert body["agent_id"] == agent_id
    assert body["to_number"] == "+221770000000"
    assert body["from_number"] == "+221780000000"


# ─── tts (binary response) ──────────────────────────────────────────────────


@respx.mock
def test_kora_synthesize_speech_returns_bytes(kora: Kora) -> None:
    # The generated TTS op still runs response.json() in _parse_response,
    # so the mocked content has to be JSON-decodable bytes. Kora's
    # _call_bytes returns .content directly, so we get those same bytes
    # back at the call site.
    audio_blob = b'{"audio_url":"https://cdn.test/x.wav"}'
    route = respx.post(f"{BASE_URL}/api/v1/tts").mock(
        return_value=httpx.Response(
            200,
            content=audio_blob,
            headers={"content-type": "application/json"},
        )
    )

    out = kora.synthesize_speech(text="Hello world", voice_id="fatima")

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == "/api/v1/tts"
    body = json.loads(req.content.decode())
    assert body["text"] == "Hello world"
    assert body["voice_id"] == "fatima"
    # _call_bytes returns the raw response body, not the parsed JSON.
    assert isinstance(out, bytes)
    assert out == audio_blob


@respx.mock
def test_kora_stream_speech_yields_chunks(kora: Kora) -> None:
    # Total payload returned from the stream endpoint.
    audio_blob = b"AAAA" * 1024  # 4 KiB
    route = respx.post(f"{BASE_URL}/api/v1/tts/stream").mock(
        return_value=httpx.Response(
            200,
            content=audio_blob,
            headers={"content-type": "audio/wav"},
        )
    )

    chunks = list(kora.stream_speech("hello", "fatima"))

    assert route.called
    # Drain the generator: concatenated chunks must match the full payload.
    assert b"".join(chunks) == audio_blob
    # And the body still carried the synthesis request.
    body = json.loads(route.calls.last.request.content.decode())
    assert body["text"] == "hello"
    assert body["voice_id"] == "fatima"


# ─── transcription (multipart) ──────────────────────────────────────────────


@respx.mock
def test_kora_transcribe_uses_multipart(kora: Kora) -> None:
    route = respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        return_value=httpx.Response(
            200,
            json={"id": "t1", "text": "hello", "language": "english"},
        )
    )

    kora.transcribe(
        b"fake-audio-bytes",
        language="english",
        file_name="audio.wav",
        mime_type="audio/wav",
    )

    assert route.called
    req = route.calls.last.request
    assert req.method == "POST"
    assert req.url.path == "/api/v1/transcribe"
    # The body must be a multipart form, not application/json.
    ctype = req.headers.get("content-type", "")
    assert ctype.startswith("multipart/form-data")


# ─── conversations ──────────────────────────────────────────────────────────


@respx.mock
def test_kora_list_conversations(kora: Kora) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/conversations").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": "c1", "agent_id": "a1"}, {"id": "c2", "agent_id": "a2"}],
                "total": 2,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = kora.list_conversations(limit=25)

    assert route.called
    req = route.calls.last.request
    assert req.url.path == "/api/v1/conversations"
    qs = dict(req.url.params)
    assert qs.get("limit") == "25"
    # PaginatedResponse exposes .data
    assert hasattr(result, "data")
    assert len(result.data) == 2


@respx.mock
def test_kora_list_conversations_filters_by_agent_client_side(kora: Kora) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/conversations").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "c1", "agent_id": "a1"},
                    {"id": "c2", "agent_id": "a2"},
                ],
                "total": 2,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = kora.list_conversations(agent_id="a1")

    assert route.called
    assert len(result.data) == 1
    assert result.data[0]["agent_id"] == "a1"


@respx.mock
def test_kora_get_conversation_audio_returns_bytes(kora: Kora) -> None:
    conv_id = uuid4()
    # As in the TTS case above, the generated op invokes response.json() to
    # build .parsed even though Kora returns .content. The mock therefore
    # has to ship JSON-decodable bytes; _call_bytes still returns the raw
    # response body.
    audio = b'{"url":"https://cdn.test/conv.wav"}'
    route = respx.get(f"{BASE_URL}/api/v1/conversations/{conv_id}/audio.wav").mock(
        return_value=httpx.Response(
            200, content=audio, headers={"content-type": "application/json"}
        )
    )

    out = kora.get_conversation_audio(conv_id)

    assert route.called
    assert out == audio
