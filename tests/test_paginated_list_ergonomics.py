"""Tests for AET-1598: paginated list ergonomics.

Verifies that ``list_agents``, ``list_calls``, and ``list_conversations``
return a ``PaginatedResponse`` that:

  1. Is iterable (``for item in result``).
  2. Supports integer indexing (``result[0]``, no ``KeyError``).
  3. Returns typed model items with typed attributes (e.g. ``.id``).

All tests mock the HTTP layer via ``respx``; no live network calls are made.
"""

from __future__ import annotations

from uuid import uuid4

import httpx
import pytest
import respx

from aethexai import AethexAI
from aethexai._generated.models.agent_response import AgentResponse
from aethexai._generated.models.call_response import CallResponse
from aethexai._generated.models.conversation_response import ConversationResponse
from aethexai._generated.models.paginated_response import PaginatedResponse

BASE_URL = "https://api.test.aethexai.com"


@pytest.fixture
def client() -> AethexAI:
    c = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    yield c
    c.close()


# ─── list_agents ────────────────────────────────────────────────────────────


@respx.mock
def test_list_agents_returns_paginated_response(client: AethexAI) -> None:
    agent_id = str(uuid4())
    respx.get(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": agent_id, "name": "Agent A"}],
                "total": 1,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_agents()

    assert isinstance(result, PaginatedResponse)


@respx.mock
def test_list_agents_is_iterable(client: AethexAI) -> None:
    agent_id_1 = str(uuid4())
    agent_id_2 = str(uuid4())
    respx.get(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": agent_id_1, "name": "Agent A"},
                    {"id": agent_id_2, "name": "Agent B"},
                ],
                "total": 2,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_agents()

    ids = [agent.id for agent in result]
    assert ids == [agent_id_1, agent_id_2]


@respx.mock
def test_list_agents_integer_indexing(client: AethexAI) -> None:
    """AET-1598: agents[0] must not raise KeyError."""
    agent_id = str(uuid4())
    respx.get(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": agent_id, "name": "Agent A"}],
                "total": 1,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_agents()

    # This must not raise KeyError (the original bug).
    first = result[0]
    assert first.id == agent_id


@respx.mock
def test_list_agents_items_are_typed_agent_response(client: AethexAI) -> None:
    agent_id = str(uuid4())
    respx.get(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": agent_id, "name": "My Agent"}],
                "total": 1,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_agents()

    assert isinstance(result[0], AgentResponse)
    assert result[0].id == agent_id
    assert result[0].name == "My Agent"


@respx.mock
def test_list_agents_len(client: AethexAI) -> None:
    respx.get(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": str(uuid4()), "name": "A"},
                    {"id": str(uuid4()), "name": "B"},
                    {"id": str(uuid4()), "name": "C"},
                ],
                "total": 3,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_agents()

    assert len(result) == 3


# ─── list_calls ─────────────────────────────────────────────────────────────


@respx.mock
def test_list_calls_integer_indexing(client: AethexAI) -> None:
    """AET-1598: calls[0] must not raise KeyError."""
    call_id = str(uuid4())
    respx.get(f"{BASE_URL}/api/v1/calls").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": call_id}],
                "total": 1,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_calls()

    first = result[0]
    assert first.id == call_id


@respx.mock
def test_list_calls_is_iterable(client: AethexAI) -> None:
    call_id_1 = str(uuid4())
    call_id_2 = str(uuid4())
    respx.get(f"{BASE_URL}/api/v1/calls").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": call_id_1}, {"id": call_id_2}],
                "total": 2,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_calls()

    ids = [call.id for call in result]
    assert ids == [call_id_1, call_id_2]


@respx.mock
def test_list_calls_items_are_typed_call_response(client: AethexAI) -> None:
    call_id = str(uuid4())
    respx.get(f"{BASE_URL}/api/v1/calls").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": call_id}],
                "total": 1,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_calls()

    assert isinstance(result[0], CallResponse)
    assert result[0].id == call_id


# ─── list_conversations ─────────────────────────────────────────────────────


@respx.mock
def test_list_conversations_integer_indexing(client: AethexAI) -> None:
    """AET-1598: conversations[0] must not raise KeyError."""
    conv_id = str(uuid4())
    respx.get(f"{BASE_URL}/api/v1/conversations").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": conv_id, "agent_id": "a1"}],
                "total": 1,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_conversations()

    first = result[0]
    assert first.id == conv_id


@respx.mock
def test_list_conversations_is_iterable(client: AethexAI) -> None:
    conv_id_1 = str(uuid4())
    conv_id_2 = str(uuid4())
    respx.get(f"{BASE_URL}/api/v1/conversations").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": conv_id_1, "agent_id": "a1"},
                    {"id": conv_id_2, "agent_id": "a2"},
                ],
                "total": 2,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_conversations()

    ids = [conv.id for conv in result]
    assert ids == [conv_id_1, conv_id_2]


@respx.mock
def test_list_conversations_items_are_typed_conversation_response(client: AethexAI) -> None:
    conv_id = str(uuid4())
    respx.get(f"{BASE_URL}/api/v1/conversations").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": conv_id, "status": "completed"}],
                "total": 1,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_conversations()

    assert isinstance(result[0], ConversationResponse)
    assert result[0].id == conv_id
    assert result[0].status == "completed"


# ─── PaginatedResponse unit tests ────────────────────────────────────────────


def test_paginated_response_empty_data_len() -> None:
    r = PaginatedResponse(data=[], total=0, limit=50, offset=0)
    assert len(r) == 0


def test_paginated_response_unset_data_len() -> None:
    from aethexai._generated.types import UNSET

    r = PaginatedResponse()
    assert r.data is UNSET
    assert len(r) == 0


def test_paginated_response_unset_data_iter() -> None:
    r = PaginatedResponse()
    assert list(r) == []


def test_paginated_response_string_key_still_works() -> None:
    """Backward-compat: string-key indexing into additional_properties."""
    r = PaginatedResponse(data=[], total=0, limit=50, offset=0)
    r["custom_field"] = "hello"
    assert r["custom_field"] == "hello"
