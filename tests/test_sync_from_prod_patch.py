"""Unit tests for the AET-1580 post-codegen patch in ``scripts/sync_from_prod.py``.

The patch is the regen-durability layer: on every ``sync_from_prod.py --apply``
the generated client is recreated from the live spec, and the patch re-runs
to keep create wrappers from regressing to ``return None`` on HTTP 201.

These tests exercise ``_patch_created_201_source`` directly against the four
shapes openapi-python-client may emit, so a future codegen change surfaces
here rather than during a prod-spec sync.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from sync_from_prod import _CREATED_201_SENTINEL, _patch_created_201_source  # noqa: E402

_STOCK_200_UNTYPED = """\
from http import HTTPStatus
from typing import Any, Optional

import httpx


def _parse_response(*, client, response: httpx.Response) -> Optional[Any]:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
"""


_STOCK_200_TYPED = """\
from http import HTTPStatus
from typing import Optional

import httpx

from ...models.some_model import SomeModel


def _parse_response(*, client, response: httpx.Response) -> Optional[SomeModel]:
    if response.status_code == 200:
        response_200 = SomeModel.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
"""


_NATIVE_201 = """\
from http import HTTPStatus
from typing import Any, Optional

import httpx


def _parse_response(*, client, response: httpx.Response) -> Optional[Any]:
    if response.status_code == 201:
        response_201 = response.json()
        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
"""


_NO_SUCCESS_BRANCH = """\
from http import HTTPStatus
from typing import Any, Optional

import httpx


def _parse_response(*, client, response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
"""


def test_patches_untyped_200_branch() -> None:
    """200-only untyped pass-through gets a mirrored 201 branch."""
    patched = _patch_created_201_source(_STOCK_200_UNTYPED)
    assert patched is not None
    assert "if response.status_code == 201:" in patched
    assert "response_201 = response.json()" in patched
    assert "return response_201" in patched
    # 200 branch is preserved alongside the new 201 branch.
    assert "if response.status_code == 200:" in patched
    assert _CREATED_201_SENTINEL in patched


def test_patches_typed_200_branch() -> None:
    """200-only typed model parse gets a mirrored 201 branch."""
    patched = _patch_created_201_source(_STOCK_200_TYPED)
    assert patched is not None
    assert "if response.status_code == 201:" in patched
    assert "response_201 = SomeModel.from_dict(response.json())" in patched
    assert "return response_201" in patched
    assert "if response.status_code == 200:" in patched


def test_skips_already_patched_file() -> None:
    """Idempotency: re-running the patch on its own output is a no-op."""
    patched = _patch_created_201_source(_STOCK_200_UNTYPED)
    assert patched is not None
    assert _patch_created_201_source(patched) is None


def test_skips_native_201_branch_from_codegen() -> None:
    """Regen-durability: once the spec declares 201, codegen emits a native
    201 branch directly. The patch must skip rather than raise (this is the
    expected steady state after openapi.json is in sync with the backend)."""
    assert _patch_created_201_source(_NATIVE_201) is None


def test_raises_when_no_success_branch_found() -> None:
    """If codegen's output shape changes so that neither a 200 nor a 201
    branch can be found, the patch must fail loudly so the regression
    surfaces during sync rather than silently leaving wrappers broken."""
    with pytest.raises(ValueError, match="could not locate the stock 200 branch"):
        _patch_created_201_source(_NO_SUCCESS_BRANCH)
