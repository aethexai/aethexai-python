"""Durability tests for the AET-1597 typed-agent-response post-codegen patch.

These tests verify that ``_patch_agent_response_source`` — the source-level helper
behind ``_apply_typed_agent_response_patch`` in ``scripts/sync_from_prod.py`` —
correctly rewrites a freshly-regenerated (untyped, ``{}``) ``_parse_response`` to
use ``AgentResponse.from_dict`` for all three agent mutation endpoints, and that
re-running the patch is idempotent.

This is the core of the reviewer's B1 concern: a future ``sync_from_prod.py --apply``
must NOT regress typed parsing even if ``openapi.json`` temporarily declares ``{}``
for any of these endpoints.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from sync_from_prod import (  # noqa: E402
    _TYPED_AGENT_RESPONSE_SENTINEL,
    _patch_agent_response_source,
)

# ---------------------------------------------------------------------------
# Simulated freshly-generated (untyped) _parse_response sources
# These represent what openapi-python-client emits when openapi.json declares
# ``{}`` (no response_model) for an endpoint.
# ---------------------------------------------------------------------------

# create_agent / duplicate_agent: POST → 201 (AET-1580 adds the 201 branch first,
# then AET-1597 upgrades both branches to typed). Simulate the state AFTER
# AET-1580 already ran (i.e. 201 branch exists but is untyped).
_UNTYPED_CREATE_POST_201_AND_200 = """\
from http import HTTPStatus
from typing import Any, Optional

import httpx

from ...models.agent_create import AgentCreate
from ...models.http_validation_error import HTTPValidationError


def _parse_response(*, client, response: httpx.Response) -> Optional[Any]:
    # AETHEX-PATCH (AET-1580): backend returns 201 Created on this resource POST
    # (aethex PR #955). Parse it exactly like 200 so the wrapper layer returns
    # the created resource instead of None. Re-applied by sync_from_prod.py.
    if response.status_code == 201:
        response_201 = response.json()
        return response_201

    if response.status_code == 200:
        response_200 = response.json()
        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())
        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
"""

# update_agent: PATCH → 200 only. Untyped.
_UNTYPED_UPDATE_PATCH_200 = """\
from http import HTTPStatus
from typing import Any, Optional

import httpx

from ...models.agent_update import AgentUpdate
from ...models.http_validation_error import HTTPValidationError


def _parse_response(*, client, response: httpx.Response) -> Optional[Any]:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())
        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
"""

# duplicate_agent with a cast-typed 200 branch (another codegen variant).
_CAST_TYPED_DUPLICATE_POST_201_AND_200 = """\
from http import HTTPStatus
from typing import Any, Optional, cast

import httpx

from ...models.http_validation_error import HTTPValidationError


def _parse_response(*, client, response: httpx.Response) -> Optional[Any]:
    # AETHEX-PATCH (AET-1580): backend returns 201 Created on this resource POST
    if response.status_code == 201:
        response_201 = cast(Any, response.json())
        return response_201

    if response.status_code == 200:
        response_200 = cast(Any, response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
"""


# ---------------------------------------------------------------------------
# Tests: create_agent / duplicate_agent (POST, success_codes=(201, 200))
# ---------------------------------------------------------------------------


def test_patch_injects_typed_201_branch_for_post_endpoint() -> None:
    """A freshly-generated untyped POST endpoint gets AgentResponse.from_dict on 201."""
    result = _patch_agent_response_source(_UNTYPED_CREATE_POST_201_AND_200, (201, 200))
    assert result is not None, "expected a patch but got None (no-op)"
    assert "AgentResponse.from_dict(response.json())" in result
    assert "response.status_code == 201" in result
    assert "response_201 = AgentResponse.from_dict(response.json())" in result
    assert _TYPED_AGENT_RESPONSE_SENTINEL in result


def test_patch_injects_typed_200_branch_for_post_endpoint() -> None:
    """A freshly-generated untyped POST endpoint also gets AgentResponse.from_dict on 200."""
    result = _patch_agent_response_source(_UNTYPED_CREATE_POST_201_AND_200, (201, 200))
    assert result is not None
    assert "response.status_code == 200" in result
    assert "response_200 = AgentResponse.from_dict(response.json())" in result


def test_patch_injects_agent_response_import_when_missing() -> None:
    """AgentResponse import is added when absent (e.g. spec was ``{}``)."""
    result = _patch_agent_response_source(_UNTYPED_CREATE_POST_201_AND_200, (201, 200))
    assert result is not None
    assert "from ...models.agent_response import AgentResponse" in result


def test_patch_cast_variant_also_typed() -> None:
    """cast(Any, response.json()) variant is also rewritten to AgentResponse.from_dict."""
    result = _patch_agent_response_source(_CAST_TYPED_DUPLICATE_POST_201_AND_200, (201, 200))
    assert result is not None
    assert "AgentResponse.from_dict(response.json())" in result
    assert "cast(Any, response.json())" not in result or result.count("AgentResponse") >= 2


# ---------------------------------------------------------------------------
# Tests: update_agent (PATCH, success_codes=(200,))
# ---------------------------------------------------------------------------


def test_patch_injects_typed_200_branch_for_patch_endpoint() -> None:
    """update_agent (PATCH 200) gets AgentResponse.from_dict — it was missing from AET-1597."""
    result = _patch_agent_response_source(_UNTYPED_UPDATE_PATCH_200, (200,))
    assert result is not None, "expected a patch but got None (no-op)"
    assert "response_200 = AgentResponse.from_dict(response.json())" in result
    assert _TYPED_AGENT_RESPONSE_SENTINEL in result


def test_patch_adds_import_for_update_agent() -> None:
    """Import is injected for update_agent too (its untyped form has no AgentResponse import)."""
    result = _patch_agent_response_source(_UNTYPED_UPDATE_PATCH_200, (200,))
    assert result is not None
    assert "from ...models.agent_response import AgentResponse" in result


# ---------------------------------------------------------------------------
# Idempotency: re-running the patch is a no-op
# ---------------------------------------------------------------------------


def test_patch_is_idempotent_for_post_endpoint() -> None:
    """Applying the patch twice is a no-op (sentinel guards the second run)."""
    first = _patch_agent_response_source(_UNTYPED_CREATE_POST_201_AND_200, (201, 200))
    assert first is not None
    second = _patch_agent_response_source(first, (201, 200))
    assert second is None, "re-running the patch on already-patched source should return None"


def test_patch_is_idempotent_for_patch_endpoint() -> None:
    """Idempotency holds for the PATCH 200 (update_agent) shape too."""
    first = _patch_agent_response_source(_UNTYPED_UPDATE_PATCH_200, (200,))
    assert first is not None
    second = _patch_agent_response_source(first, (200,))
    assert second is None, "re-running the patch on already-patched source should return None"


# ---------------------------------------------------------------------------
# All-three-ops: simulate a full regen cycle for all three endpoints
# ---------------------------------------------------------------------------


def test_all_three_ops_get_typed_parsing_after_patch() -> None:
    """All three agent ops (create/update/duplicate) get AgentResponse.from_dict after patch.

    This is the core durability guarantee: a regen from a ``{}`-schema spec
    must still produce typed branches for all three ops.
    """
    ops = [
        ("create_agent (201+200)", _UNTYPED_CREATE_POST_201_AND_200, (201, 200)),
        ("update_agent (200)", _UNTYPED_UPDATE_PATCH_200, (200,)),
        ("duplicate_agent (201+200)", _UNTYPED_CREATE_POST_201_AND_200, (201, 200)),
    ]
    for name, source, codes in ops:
        result = _patch_agent_response_source(source, codes)
        assert result is not None, f"{name}: patch returned None unexpectedly"
        assert "AgentResponse.from_dict(response.json())" in result, (
            f"{name}: AgentResponse.from_dict not found in patched source"
        )
        assert _TYPED_AGENT_RESPONSE_SENTINEL in result, (
            f"{name}: sentinel {_TYPED_AGENT_RESPONSE_SENTINEL!r} not found"
        )


def test_raises_when_primary_success_branch_missing() -> None:
    """If neither a 201 nor a 200 branch can be located, the patch raises ValueError.

    This surfaces codegen shape changes loudly rather than silently leaving
    typed parsing broken.
    """
    no_success_branch = """\
from http import HTTPStatus

import httpx


def _parse_response(*, client, response):
    if client.raise_on_unexpected_status:
        raise Exception(response.status_code)
    return None
"""
    with pytest.raises(ValueError, match="could not locate the status_code == 201 branch"):
        _patch_agent_response_source(no_success_branch, (201, 200))


# ---------------------------------------------------------------------------
# Regen round-trip tests: actual origin/main baseline sources
#
# These are the EXACT files from ``git show origin/main:src/aethexai/_generated/
# api/agents/<file>.py`` — i.e. the pre-AET-1597 state after only AET-1580 had
# run (untyped raw-dict 201/200 branches for create/duplicate, untyped 200 for
# update). Embedding them here proves that the patch function produces typed
# AgentResponse.from_dict() output from a real regen baseline (not just from
# hand-crafted synthetic inputs), and that re-running is idempotent.
# ---------------------------------------------------------------------------

# origin/main: create_agent — AET-1580 patch present (untyped 201+200 branches).
_ORIGIN_MAIN_CREATE_AGENT = """\
from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.agent_create import AgentCreate
from ...models.http_validation_error import HTTPValidationError
from typing import cast


def _get_kwargs(
    *,
    body: AgentCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/agents",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    # AETHEX-PATCH (AET-1580): backend returns 201 Created on this resource POST
    # (aethex PR #955). Parse it exactly like 200 so the wrapper layer returns
    # the created resource instead of None. Re-applied by sync_from_prod.py.
    if response.status_code == 201:
        response_201 = response.json()
        return response_201

    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None
"""

# origin/main: update_agent — purely untyped 200 branch, no AET-1580 patch.
_ORIGIN_MAIN_UPDATE_AGENT = """\
from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.agent_update import AgentUpdate
from ...models.http_validation_error import HTTPValidationError
from typing import cast
from uuid import UUID


def _get_kwargs(
    agent_id: UUID,
    *,
    body: AgentUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/agents/{agent_id}".format(
            agent_id=quote(str(agent_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None
"""

# origin/main: duplicate_agent — AET-1580 patch present (untyped 201+200 branches).
_ORIGIN_MAIN_DUPLICATE_AGENT = """\
from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from typing import cast
from uuid import UUID


def _get_kwargs(
    agent_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/agents/{agent_id}/duplicate".format(
            agent_id=quote(str(agent_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    # AETHEX-PATCH (AET-1580): backend returns 201 Created on this resource POST
    # (aethex PR #955). Parse it exactly like 200 so the wrapper layer returns
    # the created resource instead of None. Re-applied by sync_from_prod.py.
    if response.status_code == 201:
        response_201 = response.json()
        return response_201

    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None
"""


def test_regen_roundtrip_create_agent_gets_typed_parsing() -> None:
    """Round-trip: actual origin/main create_agent baseline → typed AgentResponse on 201 and 200.

    Uses the verbatim pre-AET-1597 source obtained via
    ``git show origin/main:src/aethexai/_generated/api/agents/create_agent_api_v1_agents_post.py``.
    """
    result = _patch_agent_response_source(_ORIGIN_MAIN_CREATE_AGENT, (201, 200))
    assert result is not None, "patch returned None on actual origin/main create_agent baseline"
    assert "response_201 = AgentResponse.from_dict(response.json())" in result
    assert "response_200 = AgentResponse.from_dict(response.json())" in result
    assert "from ...models.agent_response import AgentResponse" in result
    assert _TYPED_AGENT_RESPONSE_SENTINEL in result


def test_regen_roundtrip_update_agent_gets_typed_parsing() -> None:
    """Round-trip: actual origin/main update_agent baseline → typed AgentResponse on 200.

    update_agent (PATCH 200) was NOT covered by AET-1580; this test confirms the
    AET-1597 patch adds typed parsing for it. Uses the verbatim pre-AET-1597 source
    from ``git show origin/main:src/aethexai/_generated/api/agents/update_agent_api_v1_agents_agent_id_patch.py``.
    """
    result = _patch_agent_response_source(_ORIGIN_MAIN_UPDATE_AGENT, (200,))
    assert result is not None, "patch returned None on actual origin/main update_agent baseline"
    assert "response_200 = AgentResponse.from_dict(response.json())" in result
    assert "from ...models.agent_response import AgentResponse" in result
    assert _TYPED_AGENT_RESPONSE_SENTINEL in result


def test_regen_roundtrip_duplicate_agent_gets_typed_parsing() -> None:
    """Round-trip: actual origin/main duplicate_agent baseline → typed AgentResponse on 201 and 200.

    duplicate_agent stays ``{}`` in openapi.json until backend PR #1009 ships; this
    test proves the patch durably types it regardless. Uses the verbatim pre-AET-1597
    source from
    ``git show origin/main:src/aethexai/_generated/api/agents/duplicate_agent_api_v1_agents_agent_id_duplicate_post.py``.
    """
    result = _patch_agent_response_source(_ORIGIN_MAIN_DUPLICATE_AGENT, (201, 200))
    assert result is not None, "patch returned None on actual origin/main duplicate_agent baseline"
    assert "response_201 = AgentResponse.from_dict(response.json())" in result
    assert "response_200 = AgentResponse.from_dict(response.json())" in result
    assert "from ...models.agent_response import AgentResponse" in result
    assert _TYPED_AGENT_RESPONSE_SENTINEL in result


def test_regen_roundtrip_idempotent_all_three() -> None:
    """Re-running the patch on the already-patched origin/main sources is a no-op (idempotent)."""
    cases = [
        ("create_agent", _ORIGIN_MAIN_CREATE_AGENT, (201, 200)),
        ("update_agent", _ORIGIN_MAIN_UPDATE_AGENT, (200,)),
        ("duplicate_agent", _ORIGIN_MAIN_DUPLICATE_AGENT, (201, 200)),
    ]
    for name, source, codes in cases:
        first = _patch_agent_response_source(source, codes)
        assert first is not None, f"{name}: first pass returned None unexpectedly"
        second = _patch_agent_response_source(first, codes)
        assert second is None, (
            f"{name}: second pass (re-run on already-patched source) should return None"
        )
