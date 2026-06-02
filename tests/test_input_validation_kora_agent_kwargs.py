"""AET-1629(b)/AET-1631#3: Kora.create_agent / update_agent forward unknown kwargs.

Before the fix, ``Kora.create_agent`` / ``Kora.update_agent`` called
``AgentCreate(**kwargs)`` / ``AgentUpdate(**kwargs)`` directly, so any kwarg the
generated model did not declare blew up with a raw stdlib ``TypeError``
(``unexpected keyword argument``) before the request went out.

They now route through ``build_body(..., allow_extra=True)``, so unknown kwargs
are *forwarded* in the request body (forward-compat tolerance, matching the
behaviour of ``AethexAI.create_agent`` / ``update_agent``). These tests confirm:

  * an arbitrary unknown kwarg (``some_unknown_field``) no longer raises and is
    serialized into the outgoing JSON body;
  * the named convenience params on the Kora signature that do NOT exist on
    ``AgentCreate`` (e.g. ``stt_model``) forward gracefully instead of raising;
  * ``update_agent`` tolerates an unknown kwarg the same way.

These reach the network (they construct a valid body and POST/PATCH), so they
use ``@respx.mock``.
"""

from __future__ import annotations

import json
from uuid import uuid4

import httpx
import respx

from aethexai import Kora

BASE_URL = "https://api.test.aethexai.com"


def _agent_json(name: str = "Bot") -> dict[str, object]:
    """Minimal agent payload that ``AgentResponse.from_dict`` can parse."""
    return {"id": str(uuid4()), "name": name}


@respx.mock
def test_create_agent_forwards_unknown_kwarg() -> None:
    """An unknown kwarg does not raise TypeError and is forwarded in the body."""
    route = respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(200, json=_agent_json())
    )

    kora = Kora(BASE_URL, "ae_live_kora_test")
    try:
        # Pre-fix: AgentCreate(**) -> TypeError on some_unknown_field.
        agent = kora.create_agent(
            name="Bot",
            system_prompt="p",
            voice_id="v",
            some_unknown_field="x",
        )
    finally:
        kora.close()

    # Returned and parsed as a typed AgentResponse (attribute access).
    assert agent is not None
    assert agent.name == "Bot"

    assert route.called
    body = json.loads(route.calls.last.request.content)
    # The unknown field is forwarded onto the wire, not dropped.
    assert body["some_unknown_field"] == "x"
    # Declared fields still serialize correctly alongside it.
    assert body["name"] == "Bot"
    assert body["system_prompt"] == "p"
    assert body["voice_id"] == "v"


@respx.mock
def test_create_agent_unknown_named_param_stt_model_forwards() -> None:
    """``stt_model`` is on the Kora signature but not AgentCreate; it must forward."""
    route = respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(200, json=_agent_json())
    )

    kora = Kora(BASE_URL, "ae_live_kora_test")
    try:
        # Pre-fix: stt_model landed in **kwargs -> AgentCreate(**) -> TypeError.
        agent = kora.create_agent(
            name="Bot",
            system_prompt="p",
            voice_id="v",
            stt_model="whisper-x",
        )
    finally:
        kora.close()

    assert agent is not None
    assert route.called
    body = json.loads(route.calls.last.request.content)
    assert body["stt_model"] == "whisper-x"


@respx.mock
def test_create_agent_unknown_named_param_tts_model_forwards() -> None:
    """``tts_model`` is also Kora-signature-only and must forward, not raise."""
    route = respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(201, json=_agent_json())
    )

    kora = Kora(BASE_URL, "ae_live_kora_test")
    try:
        agent = kora.create_agent(
            name="Bot",
            system_prompt="p",
            voice_id="v",
            tts_model="aethex-tts-1",
        )
    finally:
        kora.close()

    assert agent is not None
    assert route.called
    body = json.loads(route.calls.last.request.content)
    assert body["tts_model"] == "aethex-tts-1"


@respx.mock
def test_create_agent_201_created_parses() -> None:
    """A 201 Created response parses the same as 200 (any-2xx success branch)."""
    route = respx.post(f"{BASE_URL}/api/v1/agents").mock(
        return_value=httpx.Response(201, json=_agent_json(name="Created"))
    )

    kora = Kora(BASE_URL, "ae_live_kora_test")
    try:
        agent = kora.create_agent(
            name="Created",
            system_prompt="p",
            voice_id="v",
            some_unknown_field="x",
        )
    finally:
        kora.close()

    assert route.called
    assert agent is not None
    assert agent.name == "Created"


@respx.mock
def test_update_agent_forwards_unknown_kwarg() -> None:
    """update_agent tolerates an unknown kwarg (no TypeError) and forwards it."""
    agent_id = str(uuid4())
    route = respx.patch(f"{BASE_URL}/api/v1/agents/{agent_id}").mock(
        return_value=httpx.Response(200, json=_agent_json())
    )

    kora = Kora(BASE_URL, "ae_live_kora_test")
    try:
        # Pre-fix: AgentUpdate(**) -> TypeError on unknown_field.
        result = kora.update_agent(agent_id, unknown_field="v")
    finally:
        kora.close()

    assert result is not None
    assert route.called
    body = json.loads(route.calls.last.request.content)
    assert body["unknown_field"] == "v"
