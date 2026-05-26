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

import json
from uuid import uuid4

import httpx
import pytest
import respx

from aethexai import AethexAI, AsyncAethexAI

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
