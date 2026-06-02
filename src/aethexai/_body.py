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
from typing import Any, TypeVar
from uuid import UUID

import attrs

from aethexai._exceptions import ValidationError

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
    except (ValueError, TypeError, AttributeError) as exc:
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

    * **Missing required fields** are reported all at once with field names.
    * **Unknown keys** are rejected by default (so a typo'd kwarg fails loudly
      instead of being silently absorbed into ``additional_properties`` and
      ignored by the server). Pass ``allow_extra=True`` for wrappers that
      intentionally forward unrecognized fields for forward-compat
      (``create_agent`` / ``update_agent``).
    * **Coercion failures** raised by the generated ``from_dict`` (a malformed
      body UUID, a wrong nested shape such as ``recipients=["+1555..."]``, a bad
      enum value) are caught and re-raised as a typed error.
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
        raise _validation_error(msg, detail)

    if not allow_extra:
        known = _known_field_names(model_cls)
        unknown = [name for name in fields if name not in known]
        if unknown:
            model_name = getattr(model_cls, "__name__", str(model_cls))
            joined = ", ".join(repr(n) for n in unknown)
            label = "field" if len(unknown) == 1 else "fields"
            msg = f"Unknown {label} for {model_name}: {joined}"
            detail = [
                {
                    "type": "unexpected_keyword_argument",
                    "loc": ["body", name],
                    "msg": "Unexpected field",
                    "input": fields,
                }
                for name in unknown
            ]
            raise _validation_error(msg, detail)

    try:
        return model_cls.from_dict(fields)  # type: ignore[attr-defined,no-any-return]
    except ValidationError:
        raise
    except (ValueError, TypeError, AttributeError) as exc:
        model_name = getattr(model_cls, "__name__", str(model_cls))
        detail = [
            {
                "type": "value_error",
                "loc": ["body"],
                "msg": str(exc),
                "input": fields,
            }
        ]
        raise _validation_error(f"Invalid value for {model_name}: {exc}", detail) from exc
