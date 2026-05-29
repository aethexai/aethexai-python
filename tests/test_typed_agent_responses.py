"""Regression tests for AET-1597: create_agent / update_agent / duplicate_agent
must return a typed ``AgentResponse`` (not a raw ``dict``).

Root cause: an incomplete fix from AET-1580 added 201 branches to
``_parse_response`` but left them returning ``response.json()`` (raw dict)
because ``openapi.json`` declared the 201 response schema as ``{}`` (untyped).
The README quickstart does ``agent = client.create_agent(...); agent.id``,
which raised ``AttributeError: 'dict' object has no attribute 'id'``.

These tests mock the HTTP layer to return a 201 (create/duplicate) or 200
(update) with a full agent body, then assert:
  1. The returned value is an ``AgentResponse`` instance (not a dict).
  2. ``agent.id`` is accessible as an attribute (not raising AttributeError).
  3. ``agent.name`` round-trips correctly.
"""

from __future__ import annotations

from uuid import uuid4

import httpx
import pytest
import respx

from aethexai import AethexAI
from aethexai._generated.models.agent_response import AgentResponse

BASE_URL = "https://api.test.aethexai.com"

_AGENT_BODY = {
    "id": "agent-aet1597",
    "name": "Bot",
    "system_prompt": "You are helpful.",
    "voice_id": "fatima",
}


@pytest.fixture
def client() -> AethexAI:
    c = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    yield c
    c.close()


# ── create_agent ──────────────────────────────────────────────────────────────


@respx.mock
def test_create_agent_201_returns_typed_agent_response(client: AethexAI) -> None:
    """create_agent must return AgentResponse on 201, not a raw dict.

    Before AET-1597: ``agent["id"]`` worked; ``agent.id`` raised AttributeError.
    After AET-1597: both work, and ``isinstance(agent, AgentResponse)`` is True.
    """
    respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(201, json=_AGENT_BODY)
    )

    agent = client.create_agent(name="Bot", system_prompt="You are helpful.", voice_id="fatima")

    assert isinstance(agent, AgentResponse), (
        f"expected AgentResponse, got {type(agent).__name__!r} — "
        "AET-1597 regression: _parse_response returned raw dict"
    )
    # This is the exact line from the README quickstart that was broken.
    assert agent.id == "agent-aet1597"
    assert agent.name == "Bot"


@respx.mock
def test_create_agent_200_returns_typed_agent_response(client: AethexAI) -> None:
    """create_agent must also return AgentResponse on a 200 response."""
    respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(200, json=_AGENT_BODY)
    )

    agent = client.create_agent(name="Bot", system_prompt="You are helpful.", voice_id="fatima")

    assert isinstance(agent, AgentResponse)
    assert agent.id == "agent-aet1597"


# ── update_agent ──────────────────────────────────────────────────────────────


@respx.mock
def test_update_agent_200_returns_typed_agent_response(client: AethexAI) -> None:
    """update_agent must return AgentResponse on 200, not a raw dict."""
    agent_uuid = uuid4()
    updated_body = {**_AGENT_BODY, "id": str(agent_uuid), "name": "Updated Bot"}
    respx.patch(f"{BASE_URL}/api/v1/agents/{agent_uuid}").mock(
        return_value=httpx.Response(200, json=updated_body)
    )

    agent = client.update_agent(agent_uuid, name="Updated Bot")

    assert isinstance(agent, AgentResponse), (
        f"expected AgentResponse, got {type(agent).__name__!r} — "
        "AET-1597 regression: update_agent _parse_response returned raw dict"
    )
    assert agent.id == str(agent_uuid)
    assert agent.name == "Updated Bot"


# ── duplicate_agent ───────────────────────────────────────────────────────────


@respx.mock
def test_duplicate_agent_201_returns_typed_agent_response(client: AethexAI) -> None:
    """duplicate_agent must return AgentResponse on 201, not a raw dict."""
    source_uuid = uuid4()
    new_uuid = str(uuid4())
    dup_body = {**_AGENT_BODY, "id": new_uuid, "name": "Bot (copy)"}
    respx.post(f"{BASE_URL}/api/v1/agents/{source_uuid}/duplicate").mock(
        return_value=httpx.Response(201, json=dup_body)
    )

    agent = client.duplicate_agent(source_uuid)

    assert isinstance(agent, AgentResponse), (
        f"expected AgentResponse, got {type(agent).__name__!r} — "
        "AET-1597 regression: duplicate_agent _parse_response returned raw dict"
    )
    assert agent.id == new_uuid
    assert agent.name == "Bot (copy)"


@respx.mock
def test_duplicate_agent_200_returns_typed_agent_response(client: AethexAI) -> None:
    """duplicate_agent must also return AgentResponse on a 200 response."""
    source_uuid = uuid4()
    dup_body = {**_AGENT_BODY, "id": str(uuid4()), "name": "Bot (copy)"}
    respx.post(f"{BASE_URL}/api/v1/agents/{source_uuid}/duplicate").mock(
        return_value=httpx.Response(200, json=dup_body)
    )

    agent = client.duplicate_agent(source_uuid)

    assert isinstance(agent, AgentResponse)
    assert agent.id == dup_body["id"]


# ── attribute access (the exact README failure mode) ──────────────────────────


@respx.mock
def test_readme_quickstart_pattern_does_not_raise(client: AethexAI) -> None:
    """Reproduce the exact README quickstart that raised AttributeError pre-fix.

    ``agent = client.create_agent(...); print(agent.id)`` must not raise.
    """
    respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(201, json=_AGENT_BODY)
    )

    # Before AET-1597 this raised: AttributeError: 'dict' object has no attribute 'id'
    agent = client.create_agent(name="Bot", system_prompt="You are helpful.", voice_id="fatima")
    agent_id = agent.id  # must not raise AttributeError

    assert agent_id == "agent-aet1597"
