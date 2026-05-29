"""Unit tests for the spec sanitizer in ``scripts/sync_from_prod.py``.

The sanitizer is the leak-prevention layer: on every ``sync_from_prod.py
--apply`` the backend's full OpenAPI dump is stripped of internal/operational
surface and scrubbed of internal commentary *before* codegen, so the shipped
SDK stays purely customer-facing while remaining functional for every public
endpoint. These tests pin that behaviour so a future change surfaces here.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from sync_from_prod import _sanitize_spec  # noqa: E402


def _spec() -> dict:
    return {
        "openapi": "3.1.0",
        "tags": [{"name": "agents"}, {"name": "internal"}, {"name": "health"}],
        "paths": {
            "/api/v1/agents": {
                "post": {
                    "tags": ["agents"],
                    "summary": "Create Agent",
                    "description": "Create an agent (AET-1566). Rows live in vo_agents. "
                    "The session is cached in Redis for fast lookup.",
                    "responses": {
                        "201": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/AgentResponse"}
                                }
                            }
                        }
                    },
                }
            },
            "/api/v1/health": {
                "get": {"tags": ["health"], "description": "Checks app.state.", "responses": {}}
            },
            "/api/v1/metrics": {"get": {"tags": ["metrics"], "responses": {}}},
            "/internal/voices": {
                "get": {
                    "tags": ["internal-admin"],
                    "description": "Auth via X-Internal-Auth dependency.",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/VoiceCatalogEntry"}
                                }
                            }
                        }
                    },
                }
            },
            "/internal/tts/voice-registry": {"get": {"tags": ["internal"], "responses": {}}},
        },
        "components": {
            "schemas": {
                "AgentResponse": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "voice": {"$ref": "#/components/schemas/VoiceRef"},
                    },
                },
                "VoiceRef": {"type": "object"},
                "VoiceCatalogEntry": {
                    "type": "object",
                    "properties": {"internal_notes": {"type": "string"}},
                },
                "Orphan": {"type": "object"},
            }
        },
    }


def test_drops_internal_and_operational_paths() -> None:
    spec = _sanitize_spec(_spec())
    assert set(spec["paths"]) == {"/api/v1/agents"}


def test_prunes_orphaned_and_internal_schemas() -> None:
    schemas = _sanitize_spec(_spec())["components"]["schemas"]
    assert "AgentResponse" in schemas  # referenced by a public route
    assert "VoiceRef" in schemas  # transitively reachable from AgentResponse
    assert "VoiceCatalogEntry" not in schemas  # only referenced by a dropped /internal route
    assert "Orphan" not in schemas  # referenced by nothing


def test_scrubs_internal_commentary() -> None:
    desc = _sanitize_spec(_spec())["paths"]["/api/v1/agents"]["post"]["description"]
    assert "AET-" not in desc
    assert "vo_" not in desc
    assert "Redis" not in desc  # whole infra sentence dropped
    assert "Create an agent" in desc  # customer-facing content preserved


def test_drops_internal_tag_declarations() -> None:
    names = {t["name"] for t in _sanitize_spec(_spec()).get("tags", [])}
    assert names == {"agents"}


def test_is_idempotent() -> None:
    once = _sanitize_spec(_spec())
    twice = _sanitize_spec(json.loads(json.dumps(once)))
    assert once == twice
