"""Regression tests: resource-creation POSTs must return the created body.

Resource-creation POSTs may answer with ``200`` or ``201``. ``_call`` decodes
the raw 2xx body via ``parse_success_body`` and does not depend on the
generated per-status ``response.parsed``, so the wrapper returns the created
resource as a plain ``dict`` regardless of which 2xx status the backend uses —
never ``None``.

These tests mock both ``200``- and ``201``-with-body responses and assert the
wrapper returns the decoded JSON body rather than ``None``.
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
    c = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    yield c
    c.close()


@respx.mock
def test_create_agent_parses_201_body(client: AethexAI) -> None:
    """Untyped (``Any``) success route: 201 body must come back, not None."""
    respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(201, json={"id": "agent-1", "name": "Bot"})
    )

    agent = client.create_agent(name="Bot", system_prompt="hi", voice_id="fatima")

    assert agent is not None
    assert agent["id"] == "agent-1"


@respx.mock
def test_conversation_connect_parses_201_body(client: AethexAI) -> None:
    """CRITICAL path behind ``Conversation.start()``: 201 must yield the session."""
    agent_id = str(uuid4())
    respx.post(f"{BASE_URL}/api/v1/conversation/connect").mock(
        return_value=httpx.Response(201, json={"session_id": "sess-1", "ice_servers": []})
    )

    session = client.conversation_connect(agent_id=agent_id)

    assert session is not None
    assert session["session_id"] == "sess-1"


@respx.mock
def test_batch_synthesize_parses_201_body(client: AethexAI) -> None:
    """Success route: 201 must yield the decoded JSON body, not None."""
    respx.post(f"{BASE_URL}/api/v1/tts/batch").mock(
        return_value=httpx.Response(
            201,
            json={
                "batch_id": "batch-1",
                "status": "pending",
                "total": 1,
                "completed": 0,
                "failed": 0,
            },
        )
    )

    result = client.batch_synthesize(items=[{"text": "hello", "voice_id": "fatima"}])

    assert result is not None
    # decoded JSON body carries the batch_id through
    assert result["batch_id"] == "batch-1"


@respx.mock
def test_create_agent_still_parses_200_body(client: AethexAI) -> None:
    """The 200 branch is preserved alongside the new 201 branch."""
    respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(200, json={"id": "agent-200", "name": "Bot"})
    )

    agent = client.create_agent(name="Bot", system_prompt="hi", voice_id="fatima")

    assert agent is not None
    assert agent["id"] == "agent-200"
