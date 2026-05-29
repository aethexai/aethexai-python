"""Guard: the shipped package must be purely customer-facing.

The committed ``openapi.json`` and every module under ``src/aethexai/`` ship to
customers (in the wheel and/or sdist). They are generated from a spec dumped off
the backend, so without active scrubbing they can leak internal routes, infra
nouns, ticket numbers, internal table/header names, and audit-doc references.
``scripts/sync_from_prod.py`` strips all of that on every sync; these tests fail
loudly if any leak slips back in.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PKG_DIR = REPO_ROOT / "src" / "aethexai"
OPENAPI = REPO_ROOT / "openapi.json"

# Patterns that must never appear in shipped artifacts. Each is a real leak
# class found in the raw backend dump; public strings (api.aethexai.com,
# AETHEX_API_KEY, developers.aethexai.com) are intentionally not matched.
FORBIDDEN = {
    "issue references": re.compile(r"\bAET-\d+\b"),
    "internal auth header": re.compile(r"X-Internal", re.IGNORECASE),
    "internal audit docs": re.compile(r"docs/audits|pre-launch-20\d\d"),
    "internal db tables": re.compile(r"\bvo_[a-z]+\b"),
    "aws account id": re.compile(r"\b918083598212\b"),
    "cluster names": re.compile(r"aethex-saas|aethex-dev"),
    "aws region": re.compile(r"eu-central-\d"),
    "developer machine path": re.compile(r"/Users/[a-z]+/"),
    "internal hostnames": re.compile(r"\.cluster\.local|\.svc\b"),
    "pr references": re.compile(r"\bPR #\d+"),
    "infra nouns": re.compile(
        r"\b(redis|vllm|omniasr|clickhouse|langfuse|coturn|pgbouncer|karpenter)\b",
        re.IGNORECASE,
    ),
    # Competitive-intelligence classes surfaced by the external-launch audit.
    "ml model names": re.compile(r"\b(qwen\w*|wav2vec\w*|nano[-_]?qwen\w*)\b", re.IGNORECASE),
    "ml model sizing": re.compile(r"\bmodel_size\b"),
    "aws managed services": re.compile(r"\b(eks|ecr|elasticache)\b", re.IGNORECASE),
    "object storage": re.compile(r"\bS3\b"),
    "queue runtime": re.compile(r"\bARQ\b"),
    "kubernetes orchestration": re.compile(r"\b(kubernetes|k8s)\b", re.IGNORECASE),
    "pod topology": re.compile(
        r"\b(pod[- ]aware|cross[- ]pod|pod routing|different pod)\b", re.IGNORECASE
    ),
    "internal config constants": re.compile(r"\bPAYG_[A-Z_]+\b"),
    "internal storage internals": re.compile(r"recording uploader|EncryptedString"),
    # WebRTC TURN/STUN provider — naming it lets a competitor infer our edge stack.
    "webrtc edge vendor": re.compile(r"cloudflare", re.IGNORECASE),
    # Lowercase ``<name>-aethex`` is an internal GitHub username; the public
    # ``X-Aethex-Signature`` webhook header is deliberately not matched.
    "engineer review notes": re.compile(r"\b[a-z]{3,}-aethex\b|\bround-\d+ MUST\b"),
}


def _shipped_python_files() -> list[Path]:
    return sorted(PKG_DIR.rglob("*.py"))


def test_openapi_has_no_internal_or_operational_paths() -> None:
    spec = json.loads(OPENAPI.read_text())
    leaked = [
        p
        for p in spec.get("paths", {})
        if p.startswith("/internal") or "/health" in p or p.endswith("/metrics")
    ]
    assert not leaked, f"internal/operational paths in shipped openapi.json: {leaked}"


def test_no_internal_references_in_shipped_files() -> None:
    targets = [
        *_shipped_python_files(),
        OPENAPI,
        REPO_ROOT / "README.md",
        REPO_ROOT / "CHANGELOG.md",
    ]
    violations: list[str] = []
    for path in targets:
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in FORBIDDEN.items():
            match = pattern.search(text)
            if match:
                rel = path.relative_to(REPO_ROOT)
                violations.append(f"{rel}: {label} -> {match.group(0)!r}")
    assert not violations, "internal info leaked into shipped artifacts:\n" + "\n".join(violations)


def test_no_internal_admin_client_modules_shipped() -> None:
    api_dir = PKG_DIR / "_generated" / "api"
    leaked = [
        d.name
        for d in api_dir.iterdir()
        if d.is_dir() and re.search(r"internal|admin|health|metric", d.name)
    ]
    assert not leaked, f"internal/admin generated client modules shipped: {leaked}"
