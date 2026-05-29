"""Tests for AET-1599: RecordingResponse.storage_path is optional.

Backend aethex#1007 removes the internal ``storage_path`` field from
``GET /recordings`` and ``GET /recordings/:id`` responses.  Before this fix the
generated ``from_dict`` did ``d.pop("storage_path")`` (no default), which raised
``KeyError`` whenever the field was absent.

Two groups of tests here:

1. **Model round-trip** — ``RecordingResponse.from_dict`` must tolerate both the
   old (field present) and new (field absent) backend shapes.
2. **Patch durability** — ``_apply_recording_storage_path_optional_patch`` from
   ``scripts/sync_from_prod.py`` must convert the stock codegen output to the
   optional form and be idempotent on re-run.  The stock source is an inline
   string (NOT a live ``git show``) so the test works on shallow CI checkouts.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from aethexai._generated.models.recording_response import RecordingResponse
from aethexai._generated.types import UNSET, Unset

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from sync_from_prod import _apply_recording_storage_path_optional_patch  # noqa: E402

# ---------------------------------------------------------------------------
# Model round-trip tests
# ---------------------------------------------------------------------------

_BASE = {
    "id": "rec_123",
    "call_id": "call_456",
}


def test_from_dict_without_storage_path_does_not_raise() -> None:
    """from_dict must succeed when the backend omits storage_path (post-#1007 shape)."""
    rec = RecordingResponse.from_dict(_BASE)
    assert rec.id == "rec_123"
    assert rec.call_id == "call_456"
    assert isinstance(rec.storage_path, Unset)


def test_from_dict_storage_path_is_unset_when_absent() -> None:
    """storage_path must be exactly UNSET (not None, not '') when omitted."""
    rec = RecordingResponse.from_dict(_BASE)
    assert rec.storage_path is UNSET


def test_from_dict_with_storage_path_still_works() -> None:
    """from_dict must still populate storage_path when the backend sends it (backward-compat)."""
    payload = {**_BASE, "storage_path": "recordings/call_456/audio.wav"}
    rec = RecordingResponse.from_dict(payload)
    assert rec.storage_path == "recordings/call_456/audio.wav"


def test_from_dict_with_all_optional_fields() -> None:
    """Full payload (all optional fields present) must parse correctly."""
    payload = {
        **_BASE,
        "storage_path": "recordings/call_456/audio.wav",
        "created_at": "2026-05-29T12:00:00Z",
        "duration_seconds": 42.5,
        "format": "wav",
        "size_bytes": 102400,
        "status": "completed",
    }
    rec = RecordingResponse.from_dict(payload)
    assert rec.id == "rec_123"
    assert rec.storage_path == "recordings/call_456/audio.wav"
    assert rec.duration_seconds == 42.5
    assert rec.status == "completed"


def test_to_dict_omits_storage_path_when_unset() -> None:
    """to_dict must not emit storage_path when it is UNSET."""
    rec = RecordingResponse.from_dict(_BASE)
    d = rec.to_dict()
    assert "storage_path" not in d


def test_to_dict_emits_storage_path_when_set() -> None:
    """to_dict must emit storage_path when a value is present (backward-compat)."""
    payload = {**_BASE, "storage_path": "recordings/call_456/audio.wav"}
    rec = RecordingResponse.from_dict(payload)
    d = rec.to_dict()
    assert d["storage_path"] == "recordings/call_456/audio.wav"


def test_construct_without_storage_path() -> None:
    """Direct construction without storage_path must work (it has a default)."""
    rec = RecordingResponse(call_id="call_1", id="rec_1")
    assert rec.storage_path is UNSET


# ---------------------------------------------------------------------------
# Patch durability round-trip tests
# ---------------------------------------------------------------------------

# Inline fixture: the stock codegen output shape for recording_response.py
# (required storage_path, no UNSET default).  Using an inline string rather
# than ``git show`` so the test works on shallow CI checkouts.
_STOCK_RECORDING_RESPONSE = '''\
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="RecordingResponse")


@_attrs_define
class RecordingResponse:
    """
    Attributes:
        call_id (str):
        id (str):
        storage_path (str):
        created_at (None | str | Unset):
        duration_seconds (float | None | Unset):
        format_ (str | Unset):  Default: \'wav\'.
        size_bytes (int | None | Unset):
        status (str | Unset):  Default: \'completed\'.
    """

    call_id: str
    id: str
    storage_path: str
    created_at: None | str | Unset = UNSET
    duration_seconds: float | None | Unset = UNSET
    format_: str | Unset = "wav"
    size_bytes: int | None | Unset = UNSET
    status: str | Unset = "completed"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call_id = self.call_id

        id = self.id

        storage_path = self.storage_path

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call_id": call_id,
                "id": id,
                "storage_path": storage_path,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        call_id = d.pop("call_id")

        id = d.pop("id")

        storage_path = d.pop("storage_path")

        created_at = d.pop("created_at", UNSET)

        recording_response = cls(
            call_id=call_id,
            id=id,
            storage_path=storage_path,
            created_at=created_at,
        )

        recording_response.additional_properties = d
        return recording_response
'''


def _run_patch_on_source(source: str, tmp_path: Path) -> str:
    """Write *source* to a temp file, run the patch function against it, return the result."""
    models_dir = tmp_path / "models"
    models_dir.mkdir(parents=True)
    target = models_dir / "recording_response.py"
    target.write_text(source)

    # Temporarily redirect GENERATED_DIR so the patch function targets our temp file.
    import sync_from_prod as _sync

    orig = _sync.GENERATED_DIR
    _sync.GENERATED_DIR = tmp_path
    try:
        rc = _apply_recording_storage_path_optional_patch()
    finally:
        _sync.GENERATED_DIR = orig

    assert rc == 0, f"patch returned non-zero exit code: {rc}"
    return target.read_text()


def test_patch_makes_storage_path_optional(tmp_path: Path) -> None:
    """Patch converts ``storage_path: str`` to ``str | Unset = UNSET``."""
    patched = _run_patch_on_source(_STOCK_RECORDING_RESPONSE, tmp_path)
    assert "storage_path: str | Unset = UNSET" in patched


def test_patch_fixes_from_dict_pop(tmp_path: Path) -> None:
    """Patch changes ``d.pop(\"storage_path\")`` to supply UNSET as default."""
    patched = _run_patch_on_source(_STOCK_RECORDING_RESPONSE, tmp_path)
    assert 'd.pop("storage_path", UNSET)' in patched
    assert 'd.pop("storage_path")' not in patched


def test_patch_adds_sentinel(tmp_path: Path) -> None:
    """Patch inserts the AETHEX-PATCH (AET-1599) sentinel."""
    patched = _run_patch_on_source(_STOCK_RECORDING_RESPONSE, tmp_path)
    assert "AETHEX-PATCH (AET-1599)" in patched


def test_patch_is_idempotent(tmp_path: Path) -> None:
    """Running the patch twice must be a no-op (sentinel guards re-application)."""
    patched_once = _run_patch_on_source(_STOCK_RECORDING_RESPONSE, tmp_path)
    # Write patched source back and run again.
    models_dir = tmp_path / "models"
    target = models_dir / "recording_response.py"
    target.write_text(patched_once)

    import sync_from_prod as _sync

    orig = _sync.GENERATED_DIR
    _sync.GENERATED_DIR = tmp_path
    try:
        rc = _apply_recording_storage_path_optional_patch()
    finally:
        _sync.GENERATED_DIR = orig

    assert rc == 0
    patched_twice = target.read_text()
    assert patched_twice == patched_once, "Second patch run modified the file (not idempotent)"


def test_patch_skips_when_field_already_absent(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """If storage_path field declaration/pop are absent (field removed from spec),
    the patch must skip cleanly without error.

    The patch checks ``if "storage_path" not in source`` — but that fires only
    when the word is completely gone.  A more realistic future state is that the
    field is gone from the class body and from_dict but the *word* may appear in
    a comment.  We test the sentinel/no-op path directly: pre-insert the sentinel
    so the patch considers the file already handled.
    """
    # Simulate "future state": sentinel already present (field handled or removed).
    already_patched = (
        "# AETHEX-PATCH (AET-1599): storage_path handled\n" + _STOCK_RECORDING_RESPONSE
    )

    models_dir = tmp_path / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    target = models_dir / "recording_response.py"
    target.write_text(already_patched)

    import sync_from_prod as _sync

    orig = _sync.GENERATED_DIR
    _sync.GENERATED_DIR = tmp_path
    try:
        rc = _apply_recording_storage_path_optional_patch()
    finally:
        _sync.GENERATED_DIR = orig

    assert rc == 0
    captured = capsys.readouterr()
    # Idempotent skip: should say "already applied"
    assert "already applied" in captured.out.lower()
    # File must be unchanged (no double-patching)
    assert target.read_text() == already_patched
