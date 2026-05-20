#!/usr/bin/env python3
"""Dump the prod Aethex backend's OpenAPI spec to a JSON file.

Imports ``aethex.main:create_app`` from a local checkout of the backend repo,
calls ``create_app().openapi()``, and writes the result to disk. Used by
``sync_from_prod.py`` (and the ``sync-check`` CI workflow) to keep the
SDK's ``openapi.json`` in lock-step with the backend.

The backend's settings model (``aethex.core.config.Settings``) treats every
field as optional with sensible defaults, but a few code paths probed during
``create_app()`` still read env vars directly. We set obviously-fake values
for the well-known ones so ``pydantic-settings`` validation and the import-time
checks both succeed; the resulting app object is only used to extract the
OpenAPI schema, never to serve traffic, so the values don't need to be real.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULT_BACKEND_PATH = "/Users/ayooluwao/aethex"
DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "openapi.json"

# Dummy env values used only to satisfy import-time validation in the backend.
# Both prefixed (AETHEX_*) and unprefixed forms are set because different
# layers of the backend read them differently (pydantic-settings uses the
# AETHEX_ prefix; a handful of legacy modules call ``os.environ.get`` without
# the prefix).
_DUMMY_ENV = {
    "ENVIRONMENT": "test",
    "AETHEX_ENVIRONMENT": "test",
    "DATABASE_URL": "sqlite:///tmp/aethex-openapi-dump.db",
    "AETHEX_DATABASE_URL": "sqlite:///tmp/aethex-openapi-dump.db",
    "JWT_SECRET": "openapi-dump-not-a-real-secret",
    "AETHEX_JWT_SECRET": "openapi-dump-not-a-real-secret",
    "STRIPE_SECRET_KEY": "sk_test_openapi_dump_not_real",
    "AETHEX_STRIPE_SECRET_KEY": "sk_test_openapi_dump_not_real",
    "AETHEX_SECRET_KEY": "openapi-dump-not-a-real-secret",
}


def _seed_env() -> None:
    """Populate dummy env vars in-place, never overwriting real values."""
    for key, value in _DUMMY_ENV.items():
        os.environ.setdefault(key, value)


def _resolve_backend_path(cli_value: str | None) -> Path:
    """Resolve backend path from CLI arg, env var, then default."""
    raw = cli_value or os.environ.get("AETHEX_BACKEND_PATH") or DEFAULT_BACKEND_PATH
    path = Path(raw).expanduser().resolve()
    if not path.is_dir():
        raise FileNotFoundError(f"Backend path does not exist or is not a directory: {path}")
    if not (path / "src" / "aethex" / "main.py").is_file():
        raise FileNotFoundError(
            f"Backend path {path} does not look like an aethex checkout "
            f"(missing src/aethex/main.py)"
        )
    return path


def dump_openapi(backend_path: Path, output: Path) -> dict[str, object]:
    """Import the backend app, call ``openapi()``, and write the JSON.

    Returns the parsed spec for downstream reporting. Raises whatever the
    import or openapi() call raises -- the wrapper script is responsible
    for translating that into a useful CLI message.
    """
    _seed_env()

    # ``cd`` so any relative paths the backend opens (alembic.ini, etc.)
    # resolve from the right root. Also prepend ``src/`` to sys.path so the
    # standard ``src``-layout import works without an editable install.
    src_dir = backend_path / "src"
    sys.path.insert(0, str(src_dir))
    os.chdir(backend_path)

    from aethex.main import create_app

    app = create_app()
    spec = app.openapi()

    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n")
    return spec


def _count_ops(spec: dict[str, object]) -> int:
    """Count operation objects (verb-level) across all paths."""
    paths = spec.get("paths") or {}
    verbs = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
    total = 0
    if isinstance(paths, dict):
        for path_item in paths.values():
            if isinstance(path_item, dict):
                total += sum(1 for verb in path_item if verb in verbs)
    return total


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint. Returns a process exit code."""
    parser = argparse.ArgumentParser(
        description="Dump the Aethex backend's OpenAPI spec to JSON.",
    )
    parser.add_argument(
        "--backend-path",
        default=None,
        help=(
            "Path to a local aethex backend checkout. "
            f"Defaults to $AETHEX_BACKEND_PATH or {DEFAULT_BACKEND_PATH}."
        ),
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help=f"Where to write the JSON spec. Defaults to {DEFAULT_OUTPUT}.",
    )
    args = parser.parse_args(argv)

    try:
        backend_path = _resolve_backend_path(args.backend_path)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    output = Path(args.output)
    try:
        spec = dump_openapi(backend_path, output)
    except Exception as exc:
        print(
            f"error: failed to import or call create_app() from {backend_path}: "
            f"{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1

    paths = spec.get("paths") or {}
    components = spec.get("components") or {}
    schemas = components.get("schemas") if isinstance(components, dict) else {}
    print(
        f"wrote {output} "
        f"(paths={len(paths) if isinstance(paths, dict) else 0}, "
        f"operations={_count_ops(spec)}, "
        f"schemas={len(schemas) if isinstance(schemas, dict) else 0})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
