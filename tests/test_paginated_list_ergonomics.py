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


# ─── AET-1628: consistent sequence protocol over .data ────────────────────────


def test_paginated_response_len_matches_data() -> None:
    """AET-1628: ``len(resp)`` equals ``len(resp.data)`` (the original bug raised
    ``TypeError: object of type 'PaginatedResponse' has no len()``)."""
    r = PaginatedResponse(data=["a", "b", "c"], total=10, limit=3, offset=0)
    assert len(r) == 3
    assert len(r) == len(r.data)


def test_paginated_response_len_unset_data_is_zero() -> None:
    r = PaginatedResponse()
    assert r.data is UNSET
    assert len(r) == 0


def test_paginated_response_len_none_data_is_zero() -> None:
    r = PaginatedResponse(data=None, total=0, limit=50, offset=0)  # type: ignore[arg-type]
    assert len(r) == 0


def test_paginated_response_iter_yields_data_items() -> None:
    """AET-1628: iteration walks ``.data`` items, in order."""
    r = PaginatedResponse(data=["a", "b", "c"], total=3, limit=3, offset=0)
    assert list(r) == ["a", "b", "c"]
    assert [item for item in r] == ["a", "b", "c"]


def test_paginated_response_iter_unset_data_is_empty() -> None:
    r = PaginatedResponse()
    assert list(r) == []


def test_paginated_response_iter_none_data_is_empty() -> None:
    r = PaginatedResponse(data=None, total=0, limit=50, offset=0)  # type: ignore[arg-type]
    assert list(r) == []


def test_paginated_response_slice_indexing_targets_data() -> None:
    r = PaginatedResponse(data=["a", "b", "c", "d"], total=4, limit=4, offset=0)
    assert r[1:3] == ["b", "c"]
    assert r[-1] == "d"


def test_paginated_response_contains_targets_data_items() -> None:
    """AET-1628: ``in`` tests membership against ``.data`` items, not
    ``additional_properties`` keys (the original bug made ``item in resp`` False
    while ``del``/``in`` operated on additional_properties)."""
    r = PaginatedResponse(data=["a", "b", "c"], total=3, limit=3, offset=0)
    assert "a" in r
    assert "z" not in r


def test_paginated_response_contains_unset_data_is_false() -> None:
    r = PaginatedResponse()
    assert "anything" not in r


def test_paginated_response_delitem_removes_data_item() -> None:
    """AET-1628: ``del resp[i]`` removes an item from ``.data`` (the original bug
    deleted from additional_properties by string key, raising KeyError on ints)."""
    r = PaginatedResponse(data=["a", "b", "c"], total=3, limit=3, offset=0)
    del r[1]
    assert r.data == ["a", "c"]
    assert len(r) == 2


def test_paginated_response_delitem_slice_removes_data_items() -> None:
    r = PaginatedResponse(data=["a", "b", "c", "d"], total=4, limit=4, offset=0)
    del r[1:3]
    assert r.data == ["a", "d"]


def test_paginated_response_delitem_unset_data_raises_index_error() -> None:
    r = PaginatedResponse()
    with pytest.raises(IndexError):
        del r[0]


def test_paginated_response_forward_compat_field_access_preserved() -> None:
    """AET-1628: forward-compat extra fields stay reachable via string-key
    subscript, the ``additional_properties`` attribute, and ``additional_keys`` —
    these are NOT affected by the sequence protocol realignment onto ``.data``."""
    r = PaginatedResponse(data=["a"], total=1, limit=50, offset=0)
    r["new_field"] = "value"  # __setitem__ -> additional_properties
    assert r["new_field"] == "value"  # str __getitem__ -> additional_properties
    assert r.additional_properties == {"new_field": "value"}
    assert r.additional_keys == ["new_field"]
    # The forward-compat key is a field, not a sequence item: ``in`` is over .data.
    assert "new_field" not in r
    assert "a" in r


def test_paginated_response_str_and_int_getitem_target_different_containers() -> None:
    """AET-1628: ``resp[int]`` -> .data item; ``resp[str]`` -> additional_properties.
    Both coexist on the same instance without collision."""
    r = PaginatedResponse(data=["item0", "item1"], total=2, limit=50, offset=0)
    r["meta"] = {"k": "v"}
    assert r[0] == "item0"  # int -> .data
    assert r["meta"] == {"k": "v"}  # str -> additional_properties


# ─── Static typing: PaginatedResponse[T] delivers per-item types ─────────────


def test_paginated_response_is_generic_agent() -> None:
    """B2 static typing: PaginatedResponse[AgentResponse] exposes AgentResponse items."""
    r: PaginatedResponse[AgentResponse] = PaginatedResponse(
        data=[AgentResponse(id="ag-1", name="Bot")], total=1, limit=50, offset=0
    )
    # Runtime check: item is an AgentResponse, not a raw dict.
    item = r.data[0]  # type: ignore[index]
    assert isinstance(item, AgentResponse)
    assert item.id == "ag-1"


def test_paginated_response_is_generic_call() -> None:
    """B2 static typing: PaginatedResponse[CallResponse] exposes CallResponse items."""
    r: PaginatedResponse[CallResponse] = PaginatedResponse(
        data=[CallResponse(id="c-1")], total=1, limit=50, offset=0
    )
    item = r.data[0]  # type: ignore[index]
    assert isinstance(item, CallResponse)
    assert item.id == "c-1"


def test_paginated_response_is_generic_conversation() -> None:
    """B2 static typing: PaginatedResponse[ConversationResponse] exposes ConversationResponse."""
    r: PaginatedResponse[ConversationResponse] = PaginatedResponse(
        data=[ConversationResponse(id="cv-1")], total=1, limit=50, offset=0
    )
    item = r.data[0]  # type: ignore[index]
    assert isinstance(item, ConversationResponse)
    assert item.id == "cv-1"
