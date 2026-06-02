"""Sync / async parity tests.

These exercise the same set of methods against ``AethexAI`` and
``AsyncAethexAI`` using a single shared respx mock per endpoint, and
assert that the two clients produce structurally identical results.

We pick a small representative subset that covers GET-list, GET-by-id,
POST-with-body, DELETE, and a binary (TTS) endpoint so that any
divergence in body shaping, URL templating, or response parsing
between the sync and async clients shows up here.
"""

from __future__ import annotations

import io
import json
import wave
from uuid import uuid4

import httpx
import pytest
import respx

import aethexai
from aethexai import AethexAI, AsyncAethexAI
from aethexai._generated.models.body_transcribe_async_api_v1_transcribe_async_post import (
    BodyTranscribeAsyncApiV1TranscribeAsyncPost,
)
from aethexai._generated.models.body_transcribe_sync_api_v1_transcribe_post import (
    BodyTranscribeSyncApiV1TranscribePost,
)
from aethexai._generated.types import File

BASE_URL = "https://api.test.aethexai.com"


# ─── helpers ────────────────────────────────────────────────────────────────


def _attrs(obj: object) -> dict[str, object]:
    """Return a dict view of an attrs-style response model for comparison."""
    if obj is None:
        return {}
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return obj.__dict__ if hasattr(obj, "__dict__") else {}


@pytest.fixture
def sync_client() -> AethexAI:
    c = AethexAI(api_key="ae_live_test", base_url=BASE_URL)
    yield c
    c.close()


@pytest.fixture
async def async_client() -> AsyncAethexAI:
    c = AsyncAethexAI(api_key="ae_live_test", base_url=BASE_URL)
    yield c
    await c.close()


# ─── list_voices ────────────────────────────────────────────────────────────


@respx.mock
async def test_parity_list_voices(sync_client: AethexAI, async_client: AsyncAethexAI) -> None:
    payload = [
        {"id": "fatima", "name": "Fatima", "language": "french"},
        {"id": "amir", "name": "Amir", "language": "arabic"},
    ]
    respx.get(f"{BASE_URL}/api/v1/voices").mock(return_value=httpx.Response(200, json=payload))

    sync_voices = sync_client.list_voices()
    async_voices = await async_client.list_voices()

    assert isinstance(sync_voices, list)
    assert isinstance(async_voices, list)
    assert len(sync_voices) == len(async_voices) == 2
    assert [v.id for v in sync_voices] == [v.id for v in async_voices]
    assert [v.name for v in sync_voices] == [v.name for v in async_voices]


# ─── list_tag_vocabulary ────────────────────────────────────────────────────


@respx.mock
async def test_parity_list_tag_vocabulary(
    sync_client: AethexAI, async_client: AsyncAethexAI
) -> None:
    payload = {
        "tone": ["warm", "calm"],
        "voice_texture": ["smooth", "deep"],
        "delivery_style": ["natural", "expressive"],
        "business_persona": ["professional", "trustworthy"],
    }
    respx.get(f"{BASE_URL}/api/v1/voices/tag-vocabulary").mock(
        return_value=httpx.Response(200, json=payload)
    )

    sync_vocab = sync_client.list_tag_vocabulary()
    async_vocab = await async_client.list_tag_vocabulary()

    assert _attrs(sync_vocab) == _attrs(async_vocab) == payload


# ─── list_countries ─────────────────────────────────────────────────────────


@respx.mock
async def test_parity_list_countries(sync_client: AethexAI, async_client: AsyncAethexAI) -> None:
    payload = [
        {"code": "NG", "name": "Nigeria"},
        {"code": "US", "name": "United States"},
    ]
    respx.get(f"{BASE_URL}/api/v1/voices/countries").mock(
        return_value=httpx.Response(200, json=payload)
    )

    sync_countries = sync_client.list_countries()
    async_countries = await async_client.list_countries()

    sync_dicts = [c.to_dict() for c in sync_countries]
    async_dicts = [c.to_dict() for c in async_countries]
    assert sync_dicts == async_dicts == payload


# ─── list_agents (paginated) ────────────────────────────────────────────────


@respx.mock
async def test_parity_list_agents(sync_client: AethexAI, async_client: AsyncAethexAI) -> None:
    payload = {
        "data": [
            {"id": "ag-1", "name": "Agent 1"},
            {"id": "ag-2", "name": "Agent 2"},
        ],
        "total": 2,
        "limit": 50,
        "offset": 0,
    }
    respx.get(f"{BASE_URL}/api/v1/agents").mock(return_value=httpx.Response(200, json=payload))

    sync_page = sync_client.list_agents()
    async_page = await async_client.list_agents()

    assert sync_page.total == async_page.total == 2
    assert len(sync_page.data) == len(async_page.data) == 2


# ─── create_agent ───────────────────────────────────────────────────────────


@respx.mock
async def test_parity_create_agent(sync_client: AethexAI, async_client: AsyncAethexAI) -> None:
    route = respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(200, json={"id": "ag-x", "name": "Bot"})
    )

    sync_out = sync_client.create_agent(name="Bot", system_prompt="Hi", voice_id="fatima")
    async_out = await async_client.create_agent(name="Bot", system_prompt="Hi", voice_id="fatima")

    # The generated op for POST /api/v1/agents returns raw JSON (Any),
    # so both clients yield equal dicts here.
    assert sync_out == async_out

    # Both clients sent identical bodies.
    assert route.call_count == 2
    body_sync = json.loads(route.calls[0].request.content.decode())
    body_async = json.loads(route.calls[1].request.content.decode())
    assert body_sync == body_async
    assert body_sync["name"] == "Bot"


# ─── get_call (single resource by id) ───────────────────────────────────────


@respx.mock
async def test_parity_get_call(sync_client: AethexAI, async_client: AsyncAethexAI) -> None:
    call_id = uuid4()
    payload = {
        "id": str(call_id),
        "agent_id": str(uuid4()),
        "to_number": "+221770000000",
        "status": "completed",
    }
    respx.get(f"{BASE_URL}/api/v1/calls/{call_id}").mock(
        return_value=httpx.Response(200, json=payload)
    )

    sync_call = sync_client.get_call(call_id)
    async_call = await async_client.get_call(call_id)

    assert sync_call.id == async_call.id == str(call_id)
    assert sync_call.status == async_call.status
    assert _attrs(sync_call) == _attrs(async_call)


# ─── synthesize_speech (binary) ─────────────────────────────────────────────


@respx.mock
async def test_parity_synthesize_speech(sync_client: AethexAI, async_client: AsyncAethexAI) -> None:
    payload = b"WAVDATA"
    respx.post(f"{BASE_URL}/api/v1/tts").mock(
        return_value=httpx.Response(200, content=payload, headers={"content-type": "audio/wav"})
    )

    sync_out = sync_client.synthesize_speech(text="hello", voice_id="fatima")
    async_out = await async_client.synthesize_speech(text="hello", voice_id="fatima")

    assert sync_out == async_out == payload


@respx.mock
async def test_parity_stream_speech(sync_client: AethexAI, async_client: AsyncAethexAI) -> None:
    payload = b"ABCD" * 1024
    respx.post(f"{BASE_URL}/api/v1/tts/stream").mock(
        return_value=httpx.Response(200, content=payload, headers={"content-type": "audio/wav"})
    )

    sync_chunks = list(sync_client.stream_speech(text="hello", voice_id="fatima", chunk_size=512))
    async_chunks = [
        chunk
        async for chunk in async_client.stream_speech(
            text="hello", voice_id="fatima", chunk_size=512
        )
    ]

    assert b"".join(sync_chunks) == b"".join(async_chunks) == payload


# ─── preview_voice / stream_audio (binary) — AET-1522 ───────────────────────


@respx.mock
async def test_parity_preview_voice(sync_client: AethexAI, async_client: AsyncAethexAI) -> None:
    payload = b"RIFF\x24\x00\x00\x00WAVE\xc0\x92\xbaPAYLOAD"
    respx.post(f"{BASE_URL}/api/v1/voices/preview").mock(
        return_value=httpx.Response(200, content=payload, headers={"content-type": "audio/wav"})
    )

    sync_out = sync_client.preview_voice(voice_id="fatima", text="hello")
    async_out = await async_client.preview_voice(voice_id="fatima", text="hello")

    assert sync_out == async_out == payload


@respx.mock
async def test_parity_stream_audio(sync_client: AethexAI, async_client: AsyncAethexAI) -> None:
    conv_id = uuid4()
    payload = b"RIFF\x24\x00\x00\x00WAVE\xc0\x92\xbaPAYLOAD"
    respx.get(f"{BASE_URL}/api/v1/conversations/{conv_id}/audio.wav").mock(
        return_value=httpx.Response(200, content=payload, headers={"content-type": "audio/wav"})
    )

    sync_out = sync_client.stream_audio(conv_id)
    async_out = await async_client.stream_audio(conv_id)

    assert sync_out == async_out == payload


# ─── delete_agent (no body) ─────────────────────────────────────────────────


@respx.mock
async def test_parity_delete_agent(sync_client: AethexAI, async_client: AsyncAethexAI) -> None:
    agent_id = uuid4()
    respx.delete(f"{BASE_URL}/api/v1/agents/{agent_id}").mock(
        return_value=httpx.Response(204, content=b"")
    )

    sync_out = sync_client.delete_agent(agent_id)
    async_out = await async_client.delete_agent(agent_id)

    # 204 -> parsed is None on both sides.
    assert sync_out is None
    assert async_out is None


# ─── cancel_transcription_job (typed response, AET-1538) ────────────────────


@respx.mock
async def test_parity_cancel_transcription_job(
    sync_client: AethexAI, async_client: AsyncAethexAI
) -> None:
    """Sync and async wrappers both return ``CancelTranscriptionJobResponse``."""
    from aethexai._generated.models.cancel_transcription_job_response import (
        CancelTranscriptionJobResponse,
    )

    job_id = uuid4()
    respx.delete(f"{BASE_URL}/api/v1/transcribe/{job_id}").mock(
        return_value=httpx.Response(200, json={"id": str(job_id), "status": "cancelled"})
    )

    sync_out = sync_client.cancel_transcription_job(job_id)
    async_out = await async_client.cancel_transcription_job(job_id)

    assert isinstance(sync_out, CancelTranscriptionJobResponse)
    assert isinstance(async_out, CancelTranscriptionJobResponse)
    assert sync_out.id == str(job_id) == async_out.id
    assert sync_out.status == async_out.status == "cancelled"


# ─── upload_knowledge_doc (multipart from friendly kwargs) ──────────────────


@respx.mock
async def test_parity_upload_knowledge_doc(
    sync_client: AethexAI, async_client: AsyncAethexAI
) -> None:
    """Sync and async wrappers build the same multipart body from friendly kwargs."""
    agent_id = uuid4()
    route = respx.post(f"{BASE_URL}/api/v1/agents/{agent_id}/knowledge-base").mock(
        return_value=httpx.Response(201, json={"id": "doc-1"})
    )

    sync_client.upload_knowledge_doc(agent_id, text="kb body", filename="Doc")
    await async_client.upload_knowledge_doc(agent_id, text="kb body", filename="Doc")

    assert route.call_count == 2
    for call in route.calls:
        assert call.request.headers.get("content-type", "").startswith("multipart/form-data")
        body = call.request.content
        assert b'name="text"' in body and b"kb body" in body
        assert b'name="filename"' in body and b"Doc" in body


# ─── transcribe_audio (WAV chunking) ────────────────────────────────────────


def _make_wav(seconds: float, rate: int = 8000) -> bytes:
    """A mono 16-bit silent WAV of the given duration."""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\x00\x00" * int(seconds * rate))
    return buffer.getvalue()


def _wav_body(seconds: float) -> BodyTranscribeSyncApiV1TranscribePost:
    """A sync-transcribe body wrapping a silent WAV of the given duration."""
    return BodyTranscribeSyncApiV1TranscribePost(
        file=File(payload=io.BytesIO(_make_wav(seconds)), file_name="a.wav", mime_type="audio/wav"),
        language="english",
    )


@respx.mock
async def test_parity_transcribe_audio_chunks_long_wav(
    sync_client: AethexAI, async_client: AsyncAethexAI
) -> None:
    """Sync and async wrappers chunk a long WAV into identical merged transcripts."""
    respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        side_effect=[
            httpx.Response(200, json={"id": "t1", "text": "alpha"}),
            httpx.Response(200, json={"id": "t2", "text": "beta"}),
            httpx.Response(200, json={"id": "t3", "text": "gamma"}),
            httpx.Response(200, json={"id": "t1", "text": "alpha"}),
            httpx.Response(200, json={"id": "t2", "text": "beta"}),
            httpx.Response(200, json={"id": "t3", "text": "gamma"}),
        ]
    )

    sync_out = sync_client.transcribe_audio(body=_wav_body(80))
    async_out = await async_client.transcribe_audio(body=_wav_body(80))

    assert sync_out.text == async_out.text == "alpha beta gamma"


def _async_wav_body(seconds: float) -> BodyTranscribeAsyncApiV1TranscribeAsyncPost:
    """An async-transcribe body wrapping a silent WAV of the given duration."""
    return BodyTranscribeAsyncApiV1TranscribeAsyncPost(
        file=File(payload=io.BytesIO(_make_wav(seconds)), file_name="a.wav", mime_type="audio/wav"),
        language="english",
    )


@respx.mock
async def test_parity_transcribe_audio_async_rejects_over_limit_wav(
    sync_client: AethexAI, async_client: AsyncAethexAI
) -> None:
    """Sync and async wrappers both pre-flight reject a >35s WAV async body."""
    respx.post(f"{BASE_URL}/api/v1/transcribe/async").mock(
        return_value=httpx.Response(200, json={"id": "j1", "status": "queued"})
    )

    with pytest.raises(aethexai.ValidationError):
        sync_client.transcribe_audio_async(body=_async_wav_body(60))
    with pytest.raises(aethexai.ValidationError):
        await async_client.transcribe_audio_async(body=_async_wav_body(60))


def _make_stereo_wav(seconds: float, rate: int = 48000) -> bytes:
    """A stereo 16-bit silent WAV of the given duration."""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\x00\x00\x00\x00" * int(seconds * rate))
    return buffer.getvalue()


def _stereo_wav_body(seconds: float, rate: int = 48000) -> BodyTranscribeSyncApiV1TranscribePost:
    """A sync-transcribe body wrapping a stereo 16-bit WAV of the given duration."""
    return BodyTranscribeSyncApiV1TranscribePost(
        file=File(
            payload=io.BytesIO(_make_stereo_wav(seconds, rate)),
            file_name="a.wav",
            mime_type="audio/wav",
        ),
        language="english",
    )


@respx.mock
async def test_parity_transcribe_audio_normalizes_stereo_48k(
    sync_client: AethexAI, async_client: AsyncAethexAI
) -> None:
    """Sync and async wrappers normalize + chunk a stereo/48k WAV into identical transcripts."""
    pytest.importorskip("av")
    respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        side_effect=[
            httpx.Response(200, json={"id": "t1", "text": "alpha"}),
            httpx.Response(200, json={"id": "t2", "text": "beta"}),
            httpx.Response(200, json={"id": "t1", "text": "alpha"}),
            httpx.Response(200, json={"id": "t2", "text": "beta"}),
        ]
    )

    sync_out = sync_client.transcribe_audio(body=_stereo_wav_body(40))
    async_out = await async_client.transcribe_audio(body=_stereo_wav_body(40))

    assert sync_out.text == async_out.text == "alpha beta"
