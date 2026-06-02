"""Body construction + input-coercion helpers for client wrappers.

The generated ``*.from_dict`` methods call ``d.pop("field")`` for every
required field, and coerce typed sub-fields (UUIDs, nested models, enums) by
calling their constructors directly. When a caller passes a malformed value,
those generated paths raise bare stdlib exceptions:

* a missing required field -> ``KeyError`` (reports only the first missing
  field, not the full set the server's 422 would list);
* a malformed body UUID / wrong nested shape / bad enum -> ``ValueError`` or
  ``TypeError`` from deep inside ``from_dict``.

A caller doing ``except aethexai.AethexError`` would miss all of these. The
helpers here funnel invalid input through a typed
:class:`aethexai.ValidationError` *before* the request goes out:

* :func:`build_body` pre-validates required fields, optionally rejects unknown
  keys, and wraps ``from_dict`` so any coercion failure surfaces as a typed
  error.
* :func:`coerce_uuid` does the same for path-parameter UUIDs.
"""

from __future__ import annotations

import builtins
import keyword
from io import BytesIO
from typing import TYPE_CHECKING, Any, BinaryIO, TypeVar
from uuid import UUID

import attrs

from aethexai._exceptions import ValidationError
from aethexai._generated.models.body_upload_knowledge_doc_api_v1_agents_agent_id_knowledge_base_post import (
    BodyUploadKnowledgeDocApiV1AgentsAgentIdKnowledgeBasePost,
)
from aethexai._generated.types import UNSET, File

if TYPE_CHECKING:
    from aethexai._generated.types import Unset

T = TypeVar("T")

# Raw audio bytes sent without an explicit file name must still carry *some*
# filename on the multipart part, otherwise the server parses the part as a
# plain form field (not a file upload) and the transcription endpoint returns
# HTTP 422. An extension-less "audio" satisfies that parsing and lets the server
# detect the real format from the leading magic bytes. Shared with ``kora.py``
# so the Kora helper and the low-level transcribe wrappers default identically.
_DEFAULT_AUDIO_FILE_NAME = "audio"


def ensure_multipart_file_name(body: T) -> T:
    """Default ``body.file.file_name`` to ``"audio"`` when the caller left it unset.

    The low-level ``transcribe_audio``/``transcribe_audio_async`` wrappers accept
    a pre-built request body whose ``file`` is a ``File``. When that ``File`` was
    constructed from raw bytes without a ``file_name``, ``File.to_tuple()`` emits
    a nameless multipart part and the server rejects it with HTTP 422. This
    mirrors the default already applied in ``kora._as_file``.

    A ``file`` whose ``file_name`` is already set is left untouched, so callers
    that pass a real filename keep their exact behaviour.

    Mutates the passed ``File``/body in place — sets ``file.file_name`` to the
    default when unset, rather than returning a copy — and returns the same body.
    """
    file = getattr(body, "file", None)
    if file is not None and not getattr(file, "file_name", None):
        file.file_name = _DEFAULT_AUDIO_FILE_NAME
    return body


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


def _known_field_names(model_cls: type) -> set[str]:
    """Return wire names of every init field on ``model_cls`` (required + optional)."""
    return {_wire_name(f.name) for f in attrs.fields(model_cls) if f.init}


def _validation_error(message: str, detail: list[dict[str, Any]]) -> ValidationError:
    """Build a typed :class:`ValidationError` with a server-shaped envelope."""
    return ValidationError(
        message=message,
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


def coerce_uuid(value: Any, field_name: str) -> UUID:
    """Coerce ``value`` to a :class:`uuid.UUID`, raising a typed error on failure.

    Path-parameter wrappers used to call ``UUID(str(value))`` directly, so a
    malformed id escaped as a stdlib ``ValueError`` (``badly formed hexadecimal
    UUID string``) before any HTTP call — invisible to ``except
    aethexai.AethexError``. This re-raises as :class:`aethexai.ValidationError`
    naming the offending path field.
    """
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except (ValueError, TypeError) as exc:
        detail = [
            {
                "type": "uuid_parsing",
                "loc": ["path", field_name],
                "msg": "Invalid UUID",
                "input": value,
            }
        ]
        raise _validation_error(
            f"Invalid UUID for path parameter {field_name!r}: {value!r}", detail
        ) from exc


def build_body(model_cls: type[T], fields: dict[str, Any], *, allow_extra: bool = False) -> T:
    """Construct ``model_cls`` from ``fields`` with a typed error on bad input.

    Equivalent to ``model_cls.from_dict(fields)`` but raises
    :class:`aethexai.ValidationError` (instead of a stdlib ``KeyError`` /
    ``ValueError`` / ``TypeError``) when input is invalid:

    * **Missing required fields and unknown keys** are reported together in one
      error — each listed in ``detail`` — mirroring the server's 422 (which
      lists every problem at once) rather than surfacing only the first
      category. (Coercion failures below can only be detected by attempting
      construction, so they remain a separate error.)
    * **Unknown keys** are rejected by default, so a typo'd kwarg fails loudly
      instead of being silently absorbed into ``additional_properties`` and
      ignored by the server. ``create_agent`` / ``update_agent`` pass
      ``allow_extra=True``: extra-kwarg tolerance on those two is a pre-existing,
      documented part of their contract (unknown fields ride through as
      ``additional_properties`` for forward-compat), so rejecting it would be a
      behavior regression. The other ``**fields`` wrappers never promised
      field-passthrough, so there a clear typo error is the better default.
    * **Coercion failures** raised by the generated ``from_dict`` (a malformed
      body UUID, a wrong nested shape such as ``recipients=["+1555..."]``, a bad
      enum value) are caught and re-raised as a typed error.
    """
    model_name = getattr(model_cls, "__name__", str(model_cls))
    missing = [name for name in _required_field_names(model_cls) if name not in fields]
    unknown = (
        []
        if allow_extra
        else [name for name in fields if name not in _known_field_names(model_cls)]
    )
    if missing or unknown:
        detail: list[dict[str, Any]] = [
            {"type": "missing", "loc": ["body", name], "msg": "Field required", "input": fields}
            for name in missing
        ]
        detail += [
            {
                "type": "unexpected_keyword_argument",
                "loc": ["body", name],
                "msg": "Unexpected field",
                "input": fields.get(name),
            }
            for name in unknown
        ]
        parts = []
        if missing:
            parts.append("missing " + ", ".join(repr(n) for n in missing))
        if unknown:
            parts.append("unknown " + ", ".join(repr(n) for n in unknown))
        raise _validation_error(f"Invalid fields for {model_name}: {'; '.join(parts)}", detail)

    try:
        return model_cls.from_dict(fields)  # type: ignore[attr-defined,no-any-return]
    except ValidationError:
        raise
    except (ValueError, TypeError) as exc:
        detail = [{"type": "value_error", "loc": ["body"], "msg": str(exc), "input": fields}]
        raise _validation_error(f"Invalid value for {model_name}: {exc}", detail) from exc


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
