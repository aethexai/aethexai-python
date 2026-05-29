"""Regen round-trip tests for the AET-1598 PaginatedResponse patch.

B1 durability guarantee: ``_patch_paginated_response_source()`` must reproduce
every hand-edit made to the committed ``paginated_response.py`` so that a
routine ``sync_from_prod.py --apply`` (which regenerates the file from scratch
and then re-runs the patch) does not clobber the single-page docstring warning,
the ``Generic[_ItemT]`` scaffolding, or the ``has_more`` / integer-``__getitem__``
ergonomics.

The tests use the stock pre-AET-1598 file contents (captured from git commit
2e2dbdb) as the "freshly regenerated" input so they do not depend on an
openapi-python-client installation.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from sync_from_prod import (  # noqa: E402
    _PAGINATED_ERGONOMICS_SENTINEL,
    _patch_paginated_response_source,
)

# ---------------------------------------------------------------------------
# Fixture: stock pre-AET-1598 paginated_response.py (from git commit 2e2dbdb)
# ---------------------------------------------------------------------------

_STOCK_PRE_1598 = subprocess.check_output(
    [
        "git",
        "show",
        "2e2dbdb:src/aethexai/_generated/models/paginated_response.py",
    ],
    cwd=str(REPO_ROOT),
    text=True,
)


# ---------------------------------------------------------------------------
# Round-trip: patch produces expected content
# ---------------------------------------------------------------------------


def test_patch_produces_generic_subclass() -> None:
    """B2: the patch must emit ``class PaginatedResponse(Generic[_ItemT])``."""
    result = _patch_paginated_response_source(_STOCK_PRE_1598)
    assert result is not None
    assert "class PaginatedResponse(Generic[_ItemT]):" in result


def test_patch_produces_item_typevar() -> None:
    """B1/B2: the patch must emit the ``_ItemT`` TypeVar declaration."""
    result = _patch_paginated_response_source(_STOCK_PRE_1598)
    assert result is not None
    assert '_ItemT = TypeVar("_ItemT")' in result


def test_patch_produces_generic_import() -> None:
    """B1/B2: the patch must add ``Generic`` to the typing import."""
    result = _patch_paginated_response_source(_STOCK_PRE_1598)
    assert result is not None
    assert "from typing import Any, Generic, TypeVar" in result


def test_patch_produces_single_page_docstring_warning() -> None:
    """B1: the patch must inject the single-page warning into the docstring."""
    result = _patch_paginated_response_source(_STOCK_PRE_1598)
    assert result is not None
    assert "**Important:**" in result
    assert ".data`` holds ONE page of results" in result


def test_patch_produces_paging_example() -> None:
    """B1: the ``while .has_more`` paging example must appear in the docstring."""
    result = _patch_paginated_response_source(_STOCK_PRE_1598)
    assert result is not None
    assert "while True:" in result
    assert "page.has_more" in result


def test_patch_produces_has_more_property() -> None:
    """B1: the patch must inject the ``has_more`` property."""
    result = _patch_paginated_response_source(_STOCK_PRE_1598)
    assert result is not None
    assert "def has_more(self) -> bool:" in result
    assert "self.offset + len(self.data) < self.total" in result


def test_patch_produces_integer_getitem() -> None:
    """B1: the patch must replace the stock string-only __getitem__ with the
    integer-over-``.data`` variant."""
    result = _patch_paginated_response_source(_STOCK_PRE_1598)
    assert result is not None
    assert "def __getitem__(self, key: int | str) -> Any:" in result
    assert "isinstance(key, int)" in result


def test_patch_produces_list_item_t_field() -> None:
    """B2: the data field must be typed as ``list[_ItemT]``, not ``list[Any]``."""
    result = _patch_paginated_response_source(_STOCK_PRE_1598)
    assert result is not None
    assert "data: list[_ItemT] | Unset = UNSET" in result


def test_patch_contains_sentinel() -> None:
    """The sentinel that makes the patch idempotent must be present."""
    result = _patch_paginated_response_source(_STOCK_PRE_1598)
    assert result is not None
    assert _PAGINATED_ERGONOMICS_SENTINEL in result


# ---------------------------------------------------------------------------
# Idempotency: re-running the patch on its own output is a no-op
# ---------------------------------------------------------------------------


def test_patch_is_idempotent() -> None:
    """Re-running the patch on an already-patched file returns None (skip)."""
    first = _patch_paginated_response_source(_STOCK_PRE_1598)
    assert first is not None, "first application must produce output"
    second = _patch_paginated_response_source(first)
    assert second is None, "second application must be a no-op (sentinel present)"


# ---------------------------------------------------------------------------
# Error path: unrecognised input shape raises ValueError
# ---------------------------------------------------------------------------


def test_patch_raises_on_missing_import() -> None:
    """If the typing import line is absent the patch raises ValueError."""
    bad_source = _STOCK_PRE_1598.replace(
        "from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator\n",
        "from typing import Any, TypeVar\n",
    )
    with pytest.raises(ValueError, match="typing import"):
        _patch_paginated_response_source(bad_source)


def test_patch_raises_on_missing_t_typevar() -> None:
    """If the ``T`` TypeVar is absent the patch raises ValueError."""
    bad_source = _STOCK_PRE_1598.replace('T = TypeVar("T", bound="PaginatedResponse")\n', "")
    with pytest.raises(ValueError, match="T TypeVar"):
        _patch_paginated_response_source(bad_source)


def test_patch_raises_on_missing_class_decl() -> None:
    """If the class declaration is absent the patch raises ValueError."""
    bad_source = _STOCK_PRE_1598.replace(
        "@_attrs_define\nclass PaginatedResponse:\n",
        "@_attrs_define\nclass PaginatedResponseWRONG:\n",
    )
    with pytest.raises(ValueError, match="class declaration"):
        _patch_paginated_response_source(bad_source)


def test_patch_raises_on_missing_docstring() -> None:
    """If the minimal codegen docstring is absent the patch raises ValueError."""
    bad_source = _STOCK_PRE_1598.replace(
        '    """\n'
        "    Attributes:\n"
        "        data (list[Any] | Unset):\n"
        "        limit (int | Unset):  Default: 50.\n"
        "        offset (int | Unset):  Default: 0.\n"
        "        total (int | Unset):  Default: 0.\n"
        '    """\n',
        '    """Custom non-standard docstring."""\n',
    )
    with pytest.raises(ValueError, match="docstring"):
        _patch_paginated_response_source(bad_source)


def test_patch_raises_on_missing_getitem() -> None:
    """If the stock __getitem__ is absent the patch raises ValueError."""
    bad_source = _STOCK_PRE_1598.replace(
        "    def __getitem__(self, key: str) -> Any:\n"
        "        return self.additional_properties[key]\n",
        "",
    )
    with pytest.raises(ValueError, match="__getitem__"):
        _patch_paginated_response_source(bad_source)
