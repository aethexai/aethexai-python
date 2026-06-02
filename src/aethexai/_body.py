"""Body construction helper for client wrappers.

The generated ``*.from_dict`` methods call ``d.pop("field")`` for every
required field. When a caller omits a required field on a wrapper like
``client.create_agent()``, ``from_dict`` raises a bare ``KeyError`` —
which obscures the fact that the request never went out and reports only
the first missing field (not the full set, like the server's 422 does).

``build_body`` pre-validates the input dict against the model's required
attrs fields and raises a typed :class:`aethexai.ValidationError` listing
every missing field before delegating to ``from_dict``.
"""

from __future__ import annotations

import builtins
import keyword
from io import BytesIO
from typing import TYPE_CHECKING, Any, BinaryIO, TypeVar

import attrs

from aethexai._exceptions import ValidationError
from aethexai._generated.models.body_upload_knowledge_doc_api_v1_agents_agent_id_knowledge_base_post import (
    BodyUploadKnowledgeDocApiV1AgentsAgentIdKnowledgeBasePost,
)
from aethexai._generated.types import UNSET, File

if TYPE_CHECKING:
    from aethexai._generated.types import Unset

T = TypeVar("T")


def _wire_name(attr_name: str) -> str:
    """Map a generated attribute name back to its JSON wire key.

    openapi-python-client suffixes ``_`` onto attribute names that collide with
    a Python keyword or builtin (the JSON ``type`` field becomes ``type_``,
    ``from`` becomes ``from_``, etc.). Wrapper methods take wire names as
    keyword arguments, so the required-field pre-check must compare against wire
    names — otherwise a required ``type`` field is always reported missing.
    """
    if attr_name.endswith("_") and (
        keyword.iskeyword(attr_name[:-1]) or hasattr(builtins, attr_name[:-1])
    ):
        return attr_name[:-1]
    return attr_name


def _required_field_names(model_cls: type) -> list[str]:
    """Return wire names of attrs fields that have no default (required at init)."""
    names: list[str] = []
    for f in attrs.fields(model_cls):
        if not f.init:
            continue
        if f.default is attrs.NOTHING:
            names.append(_wire_name(f.name))
    return names


def build_body(model_cls: type[T], fields: dict[str, Any]) -> T:
    """Construct ``model_cls`` from ``fields`` with a typed error on missing keys.

    Equivalent to ``model_cls.from_dict(fields)`` but raises
    :class:`aethexai.ValidationError` (instead of stdlib ``KeyError``) when one
    or more required fields are absent, with all missing field names listed.
    """
    required = _required_field_names(model_cls)
    missing = [name for name in required if name not in fields]
    if missing:
        model_name = getattr(model_cls, "__name__", str(model_cls))
        if len(missing) == 1:
            msg = f"Missing required field for {model_name}: {missing[0]!r}"
        else:
            joined = ", ".join(repr(n) for n in missing)
            msg = f"Missing required fields for {model_name}: {joined}"
        detail = [
            {
                "type": "missing",
                "loc": ["body", name],
                "msg": "Field required",
                "input": fields,
            }
            for name in missing
        ]
        raise ValidationError(
            message=msg,
            code="validation_error",
            status_code=422,
            response={
                "error": "Validation failed",
                "code": "validation_error",
                "request_id": None,
                "detail": detail,
                "fields": detail,
            },
        )
    return model_cls.from_dict(fields)  # type: ignore[attr-defined,no-any-return]


def _as_file(
    file: bytes | BinaryIO | File,
    *,
    file_name: str | None = None,
    mime_type: str | None = None,
) -> File:
    """Normalize raw bytes / streams / ``File`` objects into the generated ``File`` type."""
    if isinstance(file, File):
        return file
    if isinstance(file, (bytes, bytearray)):
        return File(
            payload=BytesIO(bytes(file)),
            file_name=file_name,
            mime_type=mime_type or "application/octet-stream",
        )
    return File(payload=file, file_name=file_name, mime_type=mime_type)


def build_knowledge_doc_body(
    *,
    text: str | None = None,
    file: bytes | BinaryIO | File | None = None,
    filename: str | None = None,
    file_name: str | None = None,
    mime_type: str | None = None,
) -> BodyUploadKnowledgeDocApiV1AgentsAgentIdKnowledgeBasePost:
    """Build the multipart knowledge-doc body from friendly keyword arguments.

    Provide at least one of inline ``text`` or an uploaded ``file`` (raw bytes,
    a binary stream, or a pre-built ``File``); if both are given the server
    decides which to use. ``filename`` is the stored document name; ``file_name``
    / ``mime_type`` set the uploaded part's metadata. Raises
    :class:`aethexai.ValidationError` when neither ``text`` nor ``file`` is
    supplied, so callers never need to construct the request model themselves.
    """
    if text is None and file is None:
        detail = [
            {
                "type": "missing",
                "loc": ["body", "text"],
                "msg": "Provide 'text' or 'file'.",
                "input": None,
            }
        ]
        raise ValidationError(
            message="Provide 'text' or 'file' to upload a knowledge-base document.",
            code="validation_error",
            status_code=422,
            response={
                "error": "Validation failed",
                "code": "validation_error",
                "request_id": None,
                "detail": detail,
                "fields": detail,
            },
        )
    file_field: File | Unset = (
        _as_file(file, file_name=file_name, mime_type=mime_type) if file is not None else UNSET
    )
    return BodyUploadKnowledgeDocApiV1AgentsAgentIdKnowledgeBasePost(
        file=file_field,
        filename=filename if filename is not None else UNSET,
        text=text if text is not None else UNSET,
    )
