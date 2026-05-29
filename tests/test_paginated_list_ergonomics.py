"""Tests for AET-1598: paginated list ergonomics.

Verifies that ``list_agents``, ``list_calls``, and ``list_conversations``
return a ``PaginatedResponse`` that:

  1. Supports integer indexing (``result[0]``, no ``KeyError``).
  2. Returns typed model items with typed attributes (e.g. ``.id``).
  3. Exposes ``.has_more`` correctly.
  4. Handles ``data=None`` without raising ``TypeError``.

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
from aethexai._generated.types import UNSET

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
def test_list_agents_has_more_false_when_all_on_page(client: AethexAI) -> None:
    """has_more is False when the total fits on the current page."""
    respx.get(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": str(uuid4()), "name": "A"},
                    {"id": str(uuid4()), "name": "B"},
                ],
                "total": 2,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_agents()

    assert result.has_more is False


@respx.mock
def test_list_agents_has_more_true_when_more_pages(client: AethexAI) -> None:
    """has_more is True when offset + page_size < total."""
    respx.get(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": str(uuid4()), "name": "A"}],
                "total": 100,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_agents()

    assert result.has_more is True


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


@respx.mock
def test_list_calls_has_more(client: AethexAI) -> None:
    respx.get(f"{BASE_URL}/api/v1/calls").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": str(uuid4())}],
                "total": 200,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_calls()

    assert result.has_more is True


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


@respx.mock
def test_list_conversations_has_more(client: AethexAI) -> None:
    respx.get(f"{BASE_URL}/api/v1/conversations").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [{"id": str(uuid4()), "agent_id": "a1"}],
                "total": 75,
                "limit": 50,
                "offset": 0,
            },
        )
    )

    result = client.list_conversations()

    assert result.has_more is True


# ─── PaginatedResponse unit tests ────────────────────────────────────────────


def test_paginated_response_string_key_still_works() -> None:
    """Backward-compat: string-key indexing into additional_properties."""
    r = PaginatedResponse(data=[], total=0, limit=50, offset=0)
    r["custom_field"] = "hello"
    assert r["custom_field"] == "hello"


def test_paginated_response_unset_data_raises_index_error() -> None:
    r = PaginatedResponse()
    assert r.data is UNSET
    with pytest.raises(IndexError):
        _ = r[0]


def test_paginated_response_none_data_raises_index_error() -> None:
    """m4: data=None must raise IndexError, not TypeError."""
    r = PaginatedResponse(data=None, total=0, limit=50, offset=0)  # type: ignore[arg-type]
    with pytest.raises(IndexError):
        _ = r[0]


def test_paginated_response_has_more_true() -> None:
    r = PaginatedResponse(data=[1, 2, 3], total=10, limit=3, offset=0)
    assert r.has_more is True


def test_paginated_response_has_more_false_exact_fit() -> None:
    r = PaginatedResponse(data=[1, 2, 3], total=3, limit=3, offset=0)
    assert r.has_more is False


def test_paginated_response_has_more_false_on_last_page() -> None:
    r = PaginatedResponse(data=[1], total=11, limit=10, offset=10)
    assert r.has_more is False


def test_paginated_response_has_more_unset_data_is_false() -> None:
    r = PaginatedResponse(total=100, limit=50, offset=0)
    assert r.has_more is False


def test_paginated_response_has_more_none_data_is_false() -> None:
    """m4: has_more with data=None must not raise TypeError."""
    r = PaginatedResponse(data=None, total=100, limit=50, offset=0)  # type: ignore[arg-type]
    assert r.has_more is False


def test_paginated_response_has_more_unset_total_is_false() -> None:
    r = PaginatedResponse(data=[1, 2, 3])
    # total defaults to 0 via the class default, not UNSET — so has_more = (0 + 3 < 0) = False
    assert r.has_more is False


def test_paginated_response_integer_indexing_returns_correct_item() -> None:
    r = PaginatedResponse(data=["a", "b", "c"], total=3, limit=3, offset=0)
    assert r[0] == "a"
    assert r[2] == "c"
