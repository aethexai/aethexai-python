"""Regression tests for the WebRTC signalling wrappers.

``send_offer`` / ``send_ice_candidate`` lazily import generated request models
and build their bodies through ``build_body``. A backend schema rename (or a
Python-keyword field like ``type``) that isn't reflected in the hand-written
client must surface here rather than at a customer's first live call — this is
the entry point for every WebRTC conversation, so it has to work.
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from aethexai import AethexAI, AsyncAethexAI

BASE_URL = "https://api.test.aethexai.com"
_SDP = "v=0\r\no=- 0 0 IN IP4 0.0.0.0\r\ns=-\r\nt=0 0\r\nm=audio 9 UDP/TLS/RTP/SAVPF 111\r\n"


@pytest.fixture
def client() -> AethexAI:
    c = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    yield c
    c.close()


@respx.mock
def test_send_offer_posts_sdp_and_returns_answer(client: AethexAI) -> None:
    """The ``type`` field (generated as ``type_``) must serialize, not 422 locally."""
    route = respx.post(f"{BASE_URL}/api/v1/conversation/sess-1/offer").mock(
        return_value=httpx.Response(200, json={"sdp": "v=0\r\nanswer", "type": "answer"})
    )

    result = client.send_offer("sess-1", sdp=_SDP, type="offer")

    assert route.called
    sent = json.loads(route.calls.last.request.content)
    assert sent["sdp"] == _SDP
    assert sent["type"] == "offer"
    assert result == {"sdp": "v=0\r\nanswer", "type": "answer"}


@respx.mock
def test_send_offer_missing_type_raises_validation_error(client: AethexAI) -> None:
    """Omitting a genuinely-required field still pre-flights a typed error."""
    from aethexai import ValidationError

    with pytest.raises(ValidationError, match="type"):
        client.send_offer("sess-1", sdp=_SDP)


@respx.mock
def test_send_ice_candidate_posts_candidates(client: AethexAI) -> None:
    route = respx.patch(f"{BASE_URL}/api/v1/conversation/sess-1/ice").mock(
        return_value=httpx.Response(200, json={"status": "ok"})
    )

    result = client.send_ice_candidate(
        "sess-1",
        pc_id="pc-1",
        candidates=[{"candidate": "candidate:1 1 udp ...", "sdp_mid": "0", "sdp_mline_index": 0}],
    )

    assert route.called
    assert result == {"status": "ok"}


@respx.mock
async def test_async_send_offer_handles_201() -> None:
    """Async parity, and a 201 success body comes back like a 200 would."""
    async with AsyncAethexAI(api_key="ak_live_test", base_url=BASE_URL) as client:
        respx.post(f"{BASE_URL}/api/v1/conversation/sess-2/offer").mock(
            return_value=httpx.Response(201, json={"sdp": "v=0\r\nanswer", "type": "answer"})
        )
        result = await client.send_offer("sess-2", sdp=_SDP, type="offer")
        assert result["type"] == "answer"
