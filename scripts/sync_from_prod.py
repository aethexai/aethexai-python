#!/usr/bin/env python3
"""Sync the SDK's openapi.json (and generated client) with the prod backend.

Pipeline:

    1. Run ``scripts/dump_openapi.py`` against a local backend checkout,
       writing ``openapi.json.new`` next to the existing ``openapi.json``;
       or, when ``--spec-path`` is provided, copy that already-captured
       OpenAPI spec into ``openapi.json.new``.
    2. Compute a drift report between the committed spec and the fresh one.
    3. If ``--apply``, swap the new spec into place and re-run the generator
       so ``src/aethexai/_generated/`` matches. Otherwise, print what would
       change and exit 0.

The script is intentionally tolerant of "the generator doesn't exist yet"
states: it tries ``openapi-python-client`` (which is what the layout under
``src/aethexai/_generated/`` looks like), falls back to a no-op with a
warning if the tool isn't available. The codegen agent owns wiring up the
exact regenerate command -- this script just gives them a single place to
plug it in.

Exit codes:

* ``0`` -- in-sync (or ``--apply`` succeeded).
* ``1`` -- drift detected without ``--apply`` (CI signal).
* ``2`` -- internal error (dump failed, generator blew up, etc.).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO_ROOT / "openapi.json"
NEW_SPEC_PATH = REPO_ROOT / "openapi.json.new"
GENERATED_DIR = REPO_ROOT / "src" / "aethexai" / "_generated"
DUMP_SCRIPT = Path(__file__).resolve().parent / "dump_openapi.py"


@dataclass
class Drift:
    """Structural summary of how the new spec differs from the old one."""

    added_paths: list[str]
    removed_paths: list[str]
    changed_paths: list[str]
    added_schemas: list[str]
    removed_schemas: list[str]
    changed_schemas: list[str]

    @property
    def is_empty(self) -> bool:
        return not any(
            (
                self.added_paths,
                self.removed_paths,
                self.changed_paths,
                self.added_schemas,
                self.removed_schemas,
                self.changed_schemas,
            )
        )

    def summary(self) -> str:
        if self.is_empty:
            return "no drift detected"
        return (
            f"paths: +{len(self.added_paths)} "
            f"-{len(self.removed_paths)} ~{len(self.changed_paths)} | "
            f"schemas: +{len(self.added_schemas)} "
            f"-{len(self.removed_schemas)} ~{len(self.changed_schemas)}"
        )


def _load_json(path: Path) -> dict[str, Any]:
    """Read a JSON file; empty dict if it doesn't exist."""
    if not path.is_file():
        return {}
    with path.open() as fh:
        return json.load(fh)


def _diff_keys(
    old: dict[str, Any],
    new: dict[str, Any],
) -> tuple[list[str], list[str], list[str]]:
    """Return (added, removed, changed) key lists between two dicts."""
    old_keys = set(old)
    new_keys = set(new)
    added = sorted(new_keys - old_keys)
    removed = sorted(old_keys - new_keys)
    changed = sorted(key for key in old_keys & new_keys if old[key] != new[key])
    return added, removed, changed


def compute_drift(old_spec: dict[str, Any], new_spec: dict[str, Any]) -> Drift:
    """Compare two OpenAPI specs at the path + schema level."""
    old_paths = old_spec.get("paths") or {}
    new_paths = new_spec.get("paths") or {}
    added_p, removed_p, changed_p = _diff_keys(old_paths, new_paths)

    old_schemas = ((old_spec.get("components") or {}).get("schemas")) or {}
    new_schemas = ((new_spec.get("components") or {}).get("schemas")) or {}
    added_s, removed_s, changed_s = _diff_keys(old_schemas, new_schemas)

    return Drift(
        added_paths=added_p,
        removed_paths=removed_p,
        changed_paths=changed_p,
        added_schemas=added_s,
        removed_schemas=removed_s,
        changed_schemas=changed_s,
    )


def _print_drift(drift: Drift, *, verbose: bool) -> None:
    """Render a Drift to stdout. ``verbose`` prints individual keys."""
    print(f"drift summary: {drift.summary()}")
    if not verbose or drift.is_empty:
        return

    def _section(title: str, items: list[str]) -> None:
        if items:
            print(f"  {title} ({len(items)}):")
            for item in items[:20]:
                print(f"    - {item}")
            if len(items) > 20:
                print(f"    ... and {len(items) - 20} more")

    _section("paths added", drift.added_paths)
    _section("paths removed", drift.removed_paths)
    _section("paths changed", drift.changed_paths)
    _section("schemas added", drift.added_schemas)
    _section("schemas removed", drift.removed_schemas)
    _section("schemas changed", drift.changed_schemas)


def run_dump(backend_path: str | None) -> int:
    """Invoke ``dump_openapi.py`` to produce ``openapi.json.new``.

    Returns the dump script's exit code. Stdout/stderr stream through so the
    caller sees the dump's own summary line alongside drift output.
    """
    cmd: list[str] = [
        sys.executable,
        str(DUMP_SCRIPT),
        "--output",
        str(NEW_SPEC_PATH),
    ]
    if backend_path:
        cmd.extend(["--backend-path", backend_path])
    result = subprocess.run(cmd, check=False)
    return result.returncode


def use_spec_file(spec_path: str) -> int:
    """Use an existing OpenAPI JSON file as ``openapi.json.new``.

    This is the deploy automation path: the backend workflow captures the spec
    from the running app pod, then asks the SDK repo to diff/regenerate from
    that exact deployed contract.
    """
    path = Path(spec_path).expanduser().resolve()
    if not path.is_file():
        print(f"error: spec path does not exist or is not a file: {path}", file=sys.stderr)
        return 2

    try:
        with path.open() as fh:
            spec = json.load(fh)
    except Exception as exc:
        print(
            f"error: failed to read OpenAPI spec from {path}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 2

    NEW_SPEC_PATH.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n")
    paths = spec.get("paths") or {}
    components = spec.get("components") or {}
    schemas = components.get("schemas") if isinstance(components, dict) else {}
    print(
        f"loaded {path} "
        f"(paths={len(paths) if isinstance(paths, dict) else 0}, "
        f"schemas={len(schemas) if isinstance(schemas, dict) else 0})"
    )
    return 0


def git_diff(old: Path, new: Path) -> str | None:
    """Try ``git diff --no-index`` for a human-friendly diff.

    Returns the diff text if git is available and produces output, else None.
    git's exit code is 1 when files differ, which is the expected case here.
    """
    git = shutil.which("git")
    if git is None:
        return None
    if not old.is_file():
        return None
    result = subprocess.run(
        [git, "--no-pager", "diff", "--no-index", "--stat", str(old), str(new)],
        check=False,
        capture_output=True,
        text=True,
    )
    output = (result.stdout or "") + (result.stderr or "")
    return output.strip() or None


def regenerate_client() -> int:
    """Re-run the OpenAPI client generator against the freshly-written spec.

    The SDK's ``_generated/`` directory was produced by ``openapi-python-client``
    (detectable from the ``AuthenticatedClient``/``Client`` layout). We invoke
    the tool via ``uv tool run`` so it doesn't need to be a project dep.
    If the tool isn't available, we warn and continue rather than failing --
    drift is still reported to the caller, who can decide what to do.

    Returns the generator's exit code, or 0 if we deliberately skipped.
    """
    uv = shutil.which("uv")
    if uv is None:
        print(
            "warn: uv not on PATH; skipping client regeneration. "
            "Install uv (https://docs.astral.sh/uv/) and rerun with --apply, "
            "or run the generator manually.",
            file=sys.stderr,
        )
        return 0

    # ``--meta none`` keeps the generator from rewriting pyproject.toml /
    # README; we own those files. ``--overwrite`` lets it replace the
    # existing _generated/ tree without complaining.
    # TODO(codegen-agent): if the parallel codegen agent settles on a
    # different invocation (e.g. a config file, a different tool), swap
    # this call out. The contract is: regenerate ``src/aethexai/_generated/``
    # in place from ``openapi.json``.
    cmd = [
        uv,
        "tool",
        "run",
        "--from",
        "openapi-python-client",
        "openapi-python-client",
        "generate",
        "--path",
        str(SPEC_PATH),
        "--meta",
        "none",
        "--overwrite",
        "--output-path",
        str(GENERATED_DIR),
    ]
    print(f"running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(
            f"warn: client generator exited {result.returncode}. "
            "openapi.json has still been updated; regenerate manually.",
            file=sys.stderr,
        )
        return result.returncode

    patch_rc = _apply_post_codegen_patches()
    if patch_rc != 0:
        return patch_rc
    http_patch_rc = _apply_http_validation_error_patch()
    if http_patch_rc != 0:
        return http_patch_rc
    return result.returncode


def _apply_post_codegen_patches() -> int:
    """Re-apply hand-maintained patches after openapi-python-client overwrites _generated/.

    Today there is exactly one patch: mark ``AuthenticatedClient.token`` and
    both ``Client._headers`` / ``AuthenticatedClient._headers`` as
    ``repr=False`` so the API key never appears in ``repr(client)`` /
    ``str(vars(client._client))`` / sentry breadcrumbs / pytest assertion
    failure messages. The patch is idempotent: it checks for the
    ``_SECRET_FIELDS_PATCHED`` sentinel at the top of ``_generated/client.py``
    before editing, and re-adds the sentinel + ``repr=False`` flags if missing.

    See finding A.5 in ``docs/audits/pre-launch-2026-05-17.md``.
    """
    client_py = GENERATED_DIR / "client.py"
    if not client_py.exists():
        print(f"warn: post-codegen patch skipped; {client_py} not found", file=sys.stderr)
        return 0

    source = client_py.read_text()

    if "_SECRET_FIELDS_PATCHED" in source:
        print("post-codegen patch: already applied (sentinel present)")
        return 0

    # 1. Add ``repr=False`` to the two ``_headers`` field declarations and the
    #    ``token`` field on AuthenticatedClient. Use literal string replacement
    #    with the exact codegen-shape lines — if the codegen output changes
    #    those line shapes, this will surface as a no-op-and-warn rather than
    #    a silent miss.
    replacements = [
        (
            '    _headers: dict[str, str] = field(factory=dict, kw_only=True, alias="headers")\n',
            '    _headers: dict[str, str] = field(factory=dict, kw_only=True, alias="headers", repr=False)\n',
        ),
        (
            "\n    token: str\n",
            "\n    token: str = field(repr=False)\n",
        ),
    ]
    patched = source
    misses: list[str] = []
    for needle, replacement in replacements:
        if needle not in patched:
            misses.append(needle.strip())
            continue
        # ``_headers`` appears on both Client and AuthenticatedClient, both need it.
        patched = patched.replace(needle, replacement)

    if misses:
        print(
            "warn: post-codegen patch could not locate the following lines "
            "in _generated/client.py — openapi-python-client may have changed "
            "its output shape. The API key is at risk of leaking in repr().\n"
            "Missing patterns:\n  - " + "\n  - ".join(misses),
            file=sys.stderr,
        )
        return 2

    # 2. Add the sentinel right after the imports.
    sentinel = (
        "\n# Sentinel: confirms the secret-fields-repr-suppression patch has been applied\n"
        "# to this codegen file. ``scripts/sync_from_prod.py`` re-applies the patch\n"
        "# after every ``openapi-python-client generate`` and uses this sentinel to\n"
        "# detect already-patched files. DO NOT remove without auditing every call\n"
        "# site that depends on ``token`` and the auth-header value not appearing in\n"
        "# ``repr(client)`` / structured-log output.\n"
        "_SECRET_FIELDS_PATCHED = True\n"
    )
    # Anchor on any ``from attrs import ...`` line. openapi-python-client has
    # reordered the imports between releases (e.g. ``define, evolve, field`` vs
    # ``define, field, evolve``); matching the line by prefix avoids a brittle
    # exact-string check.
    anchor_match = re.search(r"^from attrs import [^\n]*\n", patched, flags=re.MULTILINE)
    if anchor_match is None:
        print(
            "warn: post-codegen patch could not find a 'from attrs import ...' "
            "anchor; sentinel not inserted. Patch may have already partially applied.",
            file=sys.stderr,
        )
        return 2
    insert_at = anchor_match.end()
    patched = patched[:insert_at] + sentinel + patched[insert_at:]

    client_py.write_text(patched)
    print(
        "post-codegen patch: applied secret-fields-repr-suppression to "
        f"{client_py.relative_to(REPO_ROOT)}"
    )
    return 0


def _apply_http_validation_error_patch() -> int:
    """Re-apply the AET-1523 patch to ``_generated/models/http_validation_error.py``.

    The OpenAPI spec types every 422 response as FastAPI's
    ``HTTPValidationError`` (``detail: list[ValidationError]``), but the real
    aethex API returns ``{error, code, detail: <string>, request_id}``. The
    stock codegen ``from_dict`` iterates ``detail`` and calls
    ``ValidationError.from_dict(<string>)`` -> ``dict(<string>)`` -> ``ValueError``.
    That escapes ``_call`` and customers see a stdlib crash instead of
    ``aethexai.ValidationError``.

    This patch rewrites ``from_dict`` to leave ``detail`` as ``UNSET`` when it
    isn't list-of-dicts shaped and stashes the raw envelope in
    ``additional_properties``. ``_call`` then reaches
    ``_map_status_to_exception`` and raises the documented typed exception.

    The patch is idempotent: it bails out when the ``AETHEX-PATCH (AET-1523)``
    sentinel is already present.
    """
    target = GENERATED_DIR / "models" / "http_validation_error.py"
    if not target.exists():
        print(f"warn: http-validation-error patch skipped; {target} not found", file=sys.stderr)
        return 0

    source = target.read_text()
    if "aethexai-error-envelope-tolerant" in source:
        print("post-codegen patch: http-validation-error already applied (sentinel present)")
        return 0

    needle = (
        "        d = dict(src_dict)\n"
        '        _detail = d.pop("detail", UNSET)\n'
        "        detail: list[ValidationError] | Unset = UNSET\n"
        "        if _detail is not UNSET:\n"
        "            detail = []\n"
        "            for detail_item_data in _detail:\n"
        "                detail_item = ValidationError.from_dict(detail_item_data)\n"
        "\n"
        "                detail.append(detail_item)\n"
    )
    replacement = (
        "        # aethexai-error-envelope-tolerant: accept the unified error envelope on 422.\n"
        "        # The OpenAPI spec types 422 as FastAPI's ``HTTPValidationError``\n"
        "        # (``detail: list[ValidationError]``), but the real API returns\n"
        "        # ``{error, code, detail: <string>, request_id}``. Without this guard,\n"
        "        # ``ValidationError.from_dict(<string>)`` crashes with a ``ValueError``\n"
        "        # from ``dict(src_dict)``. The generated ``_parse_response`` then\n"
        "        # propagates the crash to ``_call``, which never reaches\n"
        "        # ``_map_status_to_exception`` and never raises the documented\n"
        "        # ``aethexai.ValidationError``. By leaving ``detail`` as ``UNSET`` when\n"
        "        # it isn't list-of-dicts shaped, and stashing the envelope in\n"
        "        # ``additional_properties``, ``_parse_response`` stays total: the\n"
        "        # wrapper layer sees ``response.status_code == 422`` and raises the\n"
        "        # typed exception via ``_map_status_to_exception(status, response.content, ...)``,\n"
        "        # which parses the envelope directly. This patch is re-applied by\n"
        "        # ``scripts/sync_from_prod.py`` after every regeneration.\n"
        "        d = dict(src_dict)\n"
        '        _detail = d.pop("detail", UNSET)\n'
        "        detail: list[ValidationError] | Unset = UNSET\n"
        "        if _detail is not UNSET and isinstance(_detail, list):\n"
        "            try:\n"
        "                detail = [ValidationError.from_dict(item) for item in _detail]\n"
        "            except (ValueError, TypeError, KeyError):\n"
        "                # Items don't match the FastAPI shape — stash the raw value\n"
        "                # and let the wrapper layer raise via the envelope parser.\n"
        "                detail = UNSET\n"
        '                d["detail"] = _detail\n'
        "        elif _detail is not UNSET:\n"
        "            # ``detail`` is a string / non-list — aethex envelope. Preserve\n"
        "            # the raw value in additional_properties for any caller that\n"
        '            # introspects ``http_validation_error["detail"]``.\n'
        '            d["detail"] = _detail\n'
    )
    if needle not in source:
        print(
            "warn: http-validation-error patch could not locate the stock "
            "``from_dict`` body in _generated/models/http_validation_error.py. "
            "openapi-python-client may have changed its output shape — the "
            "AET-1523 422 crash is at risk of regressing.",
            file=sys.stderr,
        )
        return 2
    target.write_text(source.replace(needle, replacement))
    print(
        "post-codegen patch: applied http-validation-error envelope tolerance to "
        f"{target.relative_to(REPO_ROOT)}"
    )
    return 0


# ── Spec sanitization ──────────────────────────────────────────────────────
#
# The committed ``openapi.json`` (and every file generated from it) ships to
# customers. The raw spec dumped from the backend's ``create_app().openapi()``
# exposes the FULL internal app: operational probes, internal/admin routes, and
# descriptions that narrate infrastructure, ticket numbers, and internal table
# names. ``_sanitize_spec`` strips that surface so the published SDK is purely
# customer-facing while staying functional for every public endpoint. It runs on
# every sync, so future dumps stay clean without manual intervention.

# Operations carrying any of these OpenAPI tags are internal/operational and
# never belong in a customer SDK.
_NON_PUBLIC_TAGS = frozenset({"internal", "internal-admin", "health", "metrics"})

# Path prefixes that are internal regardless of tagging (belt-and-suspenders).
_NON_PUBLIC_PATH_PREFIXES = ("/internal",)

_HTTP_METHODS = frozenset({"get", "put", "post", "delete", "options", "head", "patch", "trace"})

# Inline tokens that leak internal context into customer-facing text. Stripped
# wherever they appear in any description / summary / title.
_TEXT_SCRUB_PATTERNS = (
    re.compile(r"\(?\bAET-\d+(?:\s*,\s*AET-\d+)*\)?:?"),  # ticket ids
    re.compile(r"\(?\b(?:aethex\s+)?PR\s*#\d+\)?", re.IGNORECASE),  # PR refs
    re.compile(r"\(#\d+\)"),  # bare (#123)
    re.compile(r"\bmigration\s+\d+\b", re.IGNORECASE),  # migration numbers
    re.compile(r"docs/audits/\S+"),  # internal audit docs
    re.compile(r"X-Internal-[\w-]+"),  # internal auth header names
    re.compile(r"\bvo_[a-z_]+\b"),  # internal DB table names
    re.compile(r":(?:data|meth|class|func|attr|mod):`[^`]*`"),  # sphinx symbol refs
    re.compile(r"\bAETHEX_[A-Z][A-Z0-9_]*\b"),  # internal env-var names
)

# A sentence mentioning any of these infra nouns is dropped wholesale — customers
# don't need (and shouldn't see) our deployment internals.
_INFRA_SENTENCE_TERMS = re.compile(
    r"\b(redis|elasticache|postgres|clickhouse|langfuse|grafana|cloudwatch|kubernetes|"
    r"k8s|kubectl|prestop|sigterm|alb|waf|nlb|karpenter|ecr|eks|pgbouncer|coturn|"
    r"pipecat|vllm|omniasr|cloudflare|sentry|preStop)\b|app\.state",
    re.IGNORECASE,
)


# Parenthetical asides that name infrastructure, e.g. "(no WAF body inspection)".
# Dropped without losing the surrounding sentence.
_INFRA_PARENTHETICAL = re.compile(
    r"\s*\([^)]*(?:" + _INFRA_SENTENCE_TERMS.pattern + r")[^)]*\)", re.IGNORECASE
)


def _tidy_text(text: str) -> str:
    """Collapse whitespace and orphaned punctuation left behind by scrubbing."""
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"\(\s*[,;]?\s*\)", "", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _scrub_text(text: str) -> str:
    """Remove internal references from a single customer-visible string.

    Inline tokens (ticket ids, internal table names, env vars, ...) are stripped
    everywhere; parenthetical asides that name infrastructure are dropped
    without losing the surrounding sentence; any remaining infra-narrating
    sentence is dropped whole. Safety net: scrubbing never turns a non-empty
    description into an empty one — it falls back to a token-only scrub so real
    customer documentation survives.
    """
    cleaned = text
    for pattern in _TEXT_SCRUB_PATTERNS:
        cleaned = pattern.sub("", cleaned)
    cleaned = _INFRA_PARENTHETICAL.sub("", cleaned)
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    cleaned = _tidy_text(" ".join(s for s in sentences if not _INFRA_SENTENCE_TERMS.search(s)))
    if text.strip() and not cleaned.strip():
        fallback = text
        for pattern in _TEXT_SCRUB_PATTERNS:
            fallback = pattern.sub("", fallback)
        return _tidy_text(fallback)
    return cleaned


def _scrub_in_place(node: Any) -> None:
    """Recursively scrub ``description`` / ``summary`` / ``title`` strings."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("description", "summary", "title") and isinstance(value, str):
                node[key] = _scrub_text(value)
            else:
                _scrub_in_place(value)
    elif isinstance(node, list):
        for item in node:
            _scrub_in_place(item)


def _collect_schema_refs(node: Any, out: set[str]) -> None:
    """Collect every ``#/components/schemas/<Name>`` reference under ``node``."""
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
            out.add(ref.rsplit("/", 1)[-1])
        for value in node.values():
            _collect_schema_refs(value, out)
    elif isinstance(node, list):
        for item in node:
            _collect_schema_refs(item, out)


def _prune_unused_schemas(spec: dict[str, Any]) -> int:
    """Drop component schemas no longer reachable from the (sanitized) paths."""
    components = spec.get("components") or {}
    schemas = components.get("schemas") or {}
    if not schemas:
        return 0
    reachable: set[str] = set()
    _collect_schema_refs(spec.get("paths") or {}, reachable)
    for key, value in components.items():
        if key != "schemas":  # parameters / responses / requestBodies may ref schemas
            _collect_schema_refs(value, reachable)
    frontier = list(reachable)
    while frontier:
        name = frontier.pop()
        if name not in schemas:
            continue
        deps: set[str] = set()
        _collect_schema_refs(schemas[name], deps)
        for dep in deps - reachable:
            reachable.add(dep)
            frontier.append(dep)
    removed = [name for name in schemas if name not in reachable]
    for name in removed:
        del schemas[name]
    return len(removed)


def _sanitize_spec(spec: dict[str, Any]) -> dict[str, Any]:
    """Strip internal surface and scrub internal commentary from an OpenAPI spec.

    Idempotent and total: drops operations tagged internal/operational (and any
    ``/internal`` path), removes the now-unreferenced component schemas, drops
    the orphaned tag declarations, and scrubs ticket ids / internal table names /
    infra narration from every customer-visible description. Mutates and returns
    ``spec``.
    """
    paths = spec.get("paths") or {}
    dropped_ops = 0
    for path in list(paths):
        ops = paths[path]
        if not isinstance(ops, dict):
            continue
        if any(path.startswith(prefix) for prefix in _NON_PUBLIC_PATH_PREFIXES):
            dropped_ops += sum(1 for m in ops if m.lower() in _HTTP_METHODS)
            del paths[path]
            continue
        for method in list(ops):
            if method.lower() not in _HTTP_METHODS:
                continue
            op = ops[method]
            tags = set(op.get("tags") or []) if isinstance(op, dict) else set()
            if _NON_PUBLIC_TAGS & tags:
                del ops[method]
                dropped_ops += 1
        if not any(m.lower() in _HTTP_METHODS for m in ops):
            del paths[path]
    if isinstance(spec.get("tags"), list):
        spec["tags"] = [
            tag
            for tag in spec["tags"]
            if not (isinstance(tag, dict) and tag.get("name") in _NON_PUBLIC_TAGS)
        ]
    dropped_schemas = _prune_unused_schemas(spec)
    _scrub_in_place(spec)
    print(
        f"sanitized spec: dropped {dropped_ops} internal/operational operation(s) "
        f"and {dropped_schemas} orphaned schema(s)"
    )
    return spec


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint. Returns a process exit code."""
    parser = argparse.ArgumentParser(
        description=(
            "Refresh openapi.json from the prod backend and (with --apply) "
            "regenerate the client. Without --apply, exits 1 on drift so "
            "CI can fail."
        ),
    )
    parser.add_argument(
        "--backend-path",
        default=None,
        help="Forwarded to dump_openapi.py.",
    )
    parser.add_argument(
        "--spec-path",
        default=None,
        help=(
            "Use an existing OpenAPI JSON file instead of importing a backend "
            "checkout. When set, this takes precedence over --backend-path."
        ),
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Replace openapi.json with the fresh dump and regenerate the client.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print every added/removed/changed path and schema name.",
    )
    args = parser.parse_args(argv)

    dump_rc = use_spec_file(args.spec_path) if args.spec_path else run_dump(args.backend_path)
    if dump_rc != 0:
        source = "--spec-path" if args.spec_path else "dump_openapi.py"
        print(f"error: {source} failed with exit code {dump_rc}", file=sys.stderr)
        return 2

    old_spec = _load_json(SPEC_PATH)
    new_spec = _sanitize_spec(_load_json(NEW_SPEC_PATH))
    NEW_SPEC_PATH.write_text(json.dumps(new_spec, indent=2, sort_keys=True) + "\n")
    drift = compute_drift(old_spec, new_spec)

    # Show a textual stat alongside the structural drift.
    stat_output = git_diff(SPEC_PATH, NEW_SPEC_PATH)
    if stat_output:
        print("--- git diff --stat ---")
        print(stat_output)
        print("--- end diff ---")

    _print_drift(drift, verbose=args.verbose)

    if args.apply:
        NEW_SPEC_PATH.replace(SPEC_PATH)
        print(f"applied: openapi.json updated ({drift.summary()})")
        gen_rc = regenerate_client()
        if gen_rc != 0:
            return 2
        print("done")
        return 0

    # Non-apply path: keep openapi.json.new around so the developer can
    # inspect it, but signal drift via exit code for CI.
    if drift.is_empty:
        NEW_SPEC_PATH.unlink(missing_ok=True)
        print("openapi.json is in sync with the backend")
        return 0

    print(
        "openapi.json is OUT OF SYNC with the backend. "
        "Run `python scripts/sync_from_prod.py --apply` and commit.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
