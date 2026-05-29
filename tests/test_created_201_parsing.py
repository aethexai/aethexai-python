"""Regression tests for AET-1580: HTTP 201 Created responses must be parsed.

The aethex backend (PR #955 / AET-1566) now returns ``201 Created`` from
resource-creation POSTs instead of ``200 OK``. The generated
``_parse_response`` functions only branched on ``200`` and fell through to
``return None`` on ``201``; ``_call`` returns ``response.parsed`` for any 2xx,
so callers silently lost the created resource. A post-codegen patch in
``scripts/sync_from_prod.py`` adds a ``201`` branch mirroring the ``200`` one.

These tests mock a ``201``-with-body and assert the wrapper returns the parsed
value (a dict for untyped routes, a typed model for typed routes) rather than
``None``. Reverting the patch re-breaks them.
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
def test_batch_synthesize_parses_201_typed_model(client: AethexAI) -> None:
    """Typed success route: 201 must parse into the model, not return None."""
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
    # typed model carries the batch_id through
    assert result.batch_id == "batch-1"


@respx.mock
def test_create_agent_still_parses_200_body(client: AethexAI) -> None:
    """The 200 branch is preserved alongside the new 201 branch."""
    respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(200, json={"id": "agent-200", "name": "Bot"})
    )

    agent = client.create_agent(name="Bot", system_prompt="hi", voice_id="fatima")

    assert agent is not None
    assert agent["id"] == "agent-200"
