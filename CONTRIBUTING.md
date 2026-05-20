# Contributing to aethexai

Thanks for your interest in improving the official Python SDK for Aethex AI. This document walks
through the workflow we use day-to-day. If anything here is unclear or outdated, open an issue or
ping the maintainer directly (contact at the bottom).

## Getting Started

We use [uv](https://docs.astral.sh/uv/) for dependency management. Install it first, then:

```bash
git clone https://github.com/aethexai/aethexai-python.git
cd aethexai-python
uv sync --all-extras --dev
```

That installs every runtime dependency, both optional extras (`websocket`, `realtime`), and the
dev tooling (pytest, respx, ruff). All commands below assume you are inside the project root with
the venv set up by `uv`.

If you only care about the core SDK and don't intend to touch WebRTC code, you can skip the
`realtime` extra — it pulls in `aiortc`, `aioice`, and `av`, which compile native code on some
platforms:

```bash
uv sync --extra websocket --dev
```

## Running Tests

The default test suite uses `respx` to mock HTTP and runs in a few seconds:

```bash
uv run pytest
```

Use markers to scope what runs:

```bash
uv run pytest -m "not integration"   # default — pure unit tests
uv run pytest -m integration         # hits dev-api.aethexai.com, requires AETHEX_API_KEY
uv run pytest -m slow                # longer-running tests (audio, real WebRTC)
```

Integration tests look for `AETHEX_API_KEY` in the environment. If you don't have one, ping the
maintainer — we hand out scoped dev keys to contributors.

To run a single test file or a single test:

```bash
uv run pytest tests/test_kora.py
uv run pytest tests/test_kora.py::test_synthesize_speech_returns_bytes
```

## Lint and Format

Ruff handles both linting and formatting. Run before pushing:

```bash
uv run ruff check .
uv run ruff format .
```

Configuration lives in `pyproject.toml` under `[tool.ruff]`. The generated client
(`src/aethexai/_generated/`) is excluded — don't lint it, don't edit it by hand.

Type-checking with mypy:

```bash
uv run mypy src/aethexai
```

The generated package is set to `ignore_errors`, so mypy will only complain about hand-written
code.

## Pre-commit

We don't ship a pre-commit config in-tree (yet), but most contributors run a personal hook that
calls `ruff check`, `ruff format --check`, and `pytest -m "not integration"` on staged Python
files. If you want a sample `.git/hooks/pre-commit`, ask in your PR and we'll paste one.

## How the SDK is Generated

The HTTP layer in `src/aethexai/_generated/` is produced by
[openapi-python-client](https://github.com/openapi-generators/openapi-python-client) from the
production OpenAPI spec. The flow is:

1. `scripts/dump_openapi.py` — pulls the latest `openapi.json` from the production API
   (`https://api.aethexai.com/openapi.json` by default) and writes it to the repo root.
2. `scripts/sync_from_prod.py` — runs `openapi-python-client` against `openapi.json`, drops the
   result into `src/aethexai/_generated/`, then applies post-processing patches (renaming
   conflicting types, fixing import paths, etc.).

Hand-written code in `src/aethexai/` (the flat client, `kora.py`, `realtime/`, the exception
hierarchy) wraps the generated client. **Never edit `_generated/` directly** — your change will be
overwritten the next time anyone runs the sync script. If you need a behavioural fix in there,
fix it upstream or in the post-processor.

To regenerate locally:

```bash
uv run python scripts/dump_openapi.py
uv run python scripts/sync_from_prod.py
```

## Pull Request Guidelines

- Branch from `main`. Use descriptive prefixes — `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`.
- One logical change per PR. If you find yourself writing "and also" in the description, split it.
- Update `CHANGELOG.md` under `## [Unreleased]` for anything user-facing.
- New flat-client methods must come with at least one unit test under `tests/`.
- If you touch a hand-written wrapper, run the full unit suite. If you touch the generator, also
  diff `src/aethexai/_generated/` before and after and call out anything non-trivial in the PR.

PR descriptions should explain *why*, not just *what*. Reviewers can read the diff for the what.

## Release Process

Releases are tag-driven. The release workflow in `.github/workflows/` handles the build and PyPI
upload — your job as a maintainer is just to tag the right commit:

```bash
# 1. Bump version in src/aethexai/_version.py and pyproject.toml
# 2. Move Unreleased entries in CHANGELOG.md under the new version heading
# 3. Commit those changes, push to main
git tag -a v0.2.2 -m "Release 0.2.2"
git push origin v0.2.2
```

The workflow then builds the wheel + sdist and publishes to PyPI. Don't try to upload manually —
trusted publishing is configured for the workflow, not for individual accounts.

## Maintainer Contact

Maintained by the Aethex AI developer team — `developers@aethexai.com`.

For security issues, please use the disclosure process described in `SECURITY.md` instead of
opening a public issue or PR.
