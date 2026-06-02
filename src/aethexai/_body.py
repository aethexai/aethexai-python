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
from typing import Any, TypeVar

import attrs

from aethexai._exceptions import ValidationError

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
