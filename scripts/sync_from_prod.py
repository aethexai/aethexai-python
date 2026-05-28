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
    created_201_rc = _apply_created_201_patch()
    if created_201_rc != 0:
        return created_201_rc
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
        "# ``repr(client)`` / structured-log output. See"
        " ``docs/audits/pre-launch-2026-05-17.md`` finding A.5.\n"
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
    if "AETHEX-PATCH (AET-1523)" in source:
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
        "        # AETHEX-PATCH (AET-1523): tolerate the aethex unified error envelope.\n"
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


# AET-1580: resource-creation endpoints whose backend returns HTTP 201 Created
# (aethex PR #955 / AET-1566). Once ``openapi.json`` declares ``201`` for these
# routes, openapi-python-client emits a native ``201`` branch and the patch is
# a no-op skip. The list and patch remain as a defensive net: if a future spec
# dump regresses to ``200``-only, or codegen reverts to a 200-only shape, the
# patch re-applies the ``201`` branch so create wrappers don't silently return
# ``None``. Each path is relative to ``src/aethexai/_generated/api/``; keep it
# in sync with the ``status_code=201`` resource-creation routes in the backend.
_CREATED_201_ENDPOINTS = (
    "agents/create_agent_api_v1_agents_post.py",
    "agents/duplicate_agent_api_v1_agents_agent_id_duplicate_post.py",
    "agents/add_tool_api_v1_agents_agent_id_tools_post.py",
    "agents/upload_knowledge_doc_api_v1_agents_agent_id_knowledge_base_post.py",
    "agents/upload_knowledge_doc_by_upload_api_v1_agents_agent_id_knowledge_base_by_upload_post.py",
    "api_keys/create_api_key_api_v1_api_keys_post.py",
    "calls/create_call_record_api_v1_calls_post.py",
    "calls/batch_calls_api_v1_calls_batch_post.py",
    "conversation/connect_api_v1_conversation_connect_post.py",
    "dashboard/create_my_api_key_api_v1_dashboard_api_keys_post.py",
    "phone_numbers/register_twilio_api_v1_phone_numbers_twilio_register_post.py",
    "phone_numbers/register_sip_api_v1_phone_numbers_sip_register_post.py",
    "tts/batch_synthesize_api_v1_tts_batch_post.py",
)

_CREATED_201_SENTINEL = "# AETHEX-PATCH (AET-1580)"


def _patch_created_201_source(source: str) -> str | None:
    """Add a ``201`` branch mirroring the ``200`` branch in a ``_parse_response``.

    Returns the patched source, ``None`` if no patch is needed (file already
    patched, or codegen already produced a native ``201`` branch from a
    spec that declares ``201``), or raises ``ValueError`` if neither a ``200``
    nor a ``201`` branch can be located -- indicating openapi-python-client's
    output shape changed in an unexpected way.

    openapi-python-client emits the success branch as either an untyped
    pass-through::

        if response.status_code == 200:
            response_200 = response.json()
            return response_200

    or a typed model parse::

        if response.status_code == 200:
            response_200 = SomeModel.from_dict(response.json())

            return response_200

    Both forms are duplicated verbatim with ``200`` -> ``201`` so a 201 Created
    response is parsed into the same model (or raw body) instead of falling
    through to ``return None``.
    """
    if _CREATED_201_SENTINEL in source:
        return None
    if re.search(r"^ {4}if response\.status_code == 201:", source, re.MULTILINE):
        # Codegen produced a native 201 branch directly (the spec declares 201
        # for this route). Nothing to patch -- this is the expected steady
        # state after openapi.json is in sync with the backend.
        return None

    match = re.search(
        r"( {4}if response\.status_code == 200:\n(?: {8}.*\n|\n)*? {8}return response_200\n)",
        source,
    )
    if match is None:
        raise ValueError("could not locate the stock 200 branch in _parse_response")

    block_200 = match.group(1)
    block_201 = (
        f"    {_CREATED_201_SENTINEL}: backend returns 201 Created on this resource POST\n"
        "    # (aethex PR #955). Parse it exactly like 200 so the wrapper layer returns\n"
        "    # the created resource instead of None. Re-applied by sync_from_prod.py.\n"
        + block_200.replace("status_code == 200", "status_code == 201").replace(
            "response_200", "response_201"
        )
    )
    insert_at = match.start()
    return source[:insert_at] + block_201 + "\n" + source[insert_at:]


def _apply_created_201_patch() -> int:
    """Re-apply the AET-1580 patch: parse HTTP 201 create responses like 200.

    Idempotent via the ``AETHEX-PATCH (AET-1580)`` sentinel. Each target file is
    patched independently; a single miss is fatal (return 2) so the regression
    surfaces loudly rather than silently letting create wrappers return ``None``.
    """
    api_dir = GENERATED_DIR / "api"
    patched = 0
    for rel in _CREATED_201_ENDPOINTS:
        target = api_dir / rel
        if not target.exists():
            print(
                f"warn: created-201 patch could not find {target.relative_to(REPO_ROOT)}; "
                "the endpoint may have been renamed or removed. Update "
                "_CREATED_201_ENDPOINTS in scripts/sync_from_prod.py.",
                file=sys.stderr,
            )
            return 2
        source = target.read_text()
        try:
            new_source = _patch_created_201_source(source)
        except ValueError as exc:
            print(
                f"warn: created-201 patch failed for {target.relative_to(REPO_ROOT)}: {exc}. "
                "openapi-python-client may have changed its output shape — the AET-1580 "
                "201 fix is at risk of regressing.",
                file=sys.stderr,
            )
            return 2
        if new_source is None:
            continue  # already patched
        target.write_text(new_source)
        patched += 1
    print(f"post-codegen patch: applied created-201 handling to {patched} endpoint(s)")
    return 0


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
    new_spec = _load_json(NEW_SPEC_PATH)
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
