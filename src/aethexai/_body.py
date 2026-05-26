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

from typing import Any, TypeVar

import attrs

from aethexai._exceptions import ValidationError

T = TypeVar("T")


def _required_field_names(model_cls: type) -> list[str]:
    """Return names of attrs fields that have no default (i.e. required at init)."""
    names: list[str] = []
    for f in attrs.fields(model_cls):
        if not f.init:
            continue
        if f.default is attrs.NOTHING:
            names.append(f.name)
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
        # Mirror the server's 422 envelope so callers can write one handler
        # that iterates `response["detail"]` regardless of whether the error
        # came from the SDK pre-flight or the server.
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
            response={"code": "validation_error", "detail": detail, "fields": detail},
        )
    return model_cls.from_dict(fields)  # type: ignore[attr-defined,no-any-return]
