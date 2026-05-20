# Security Policy

The Aethex AI team takes the security of this SDK and the services it talks to
seriously. We appreciate responsible disclosure from security researchers and
the wider community.

## Supported Versions

Security fixes are currently provided for the latest minor release line.

| Version  | Supported          |
| -------- | ------------------ |
| 0.2.x    | :white_check_mark: |
| < 0.2.0  | :x:                |

When a new minor line ships (e.g. 0.3.x), the previous line receives security
fixes for at least 30 days to give downstream users time to upgrade.

## Reporting a Vulnerability

Please **do not** open public GitHub issues for security reports.

Instead, email a detailed report to:

<!-- TODO: confirm/provision this mailbox before publishing the next release. -->
**security@aethexai.com**

Include, where possible:

- A description of the issue and the affected component(s)
- A minimal reproduction (code snippet, request, or proof-of-concept)
- The SDK version (`aethexai.__version__`) and Python version
- The potential impact as you see it

If you would like to encrypt your report, request our PGP key in your first
message and we will reply with one.

## Scope

**In scope**

- The `aethexai` package source under `src/aethexai/` (excluding the
  auto-generated client under `src/aethexai/_generated/`, which is regenerated
  from `openapi.json` upstream)
- Examples and helper scripts under `examples/` and `scripts/`
- CI workflows under `.github/workflows/` (e.g. accidental secret exposure)

**Out of scope**

- Issues that only affect end-of-life Python versions (< 3.10)
- Denial-of-service against your own account (rate-limit yourself)
- Findings derived purely from reading public API documentation
- Vulnerabilities in upstream dependencies that have not yet been patched
  upstream (please report those to the relevant maintainers)

## Response Timeline

- **Acknowledgement:** within **48 hours** of receipt
- **Initial assessment:** within **5 business days**
- **Fix or coordinated disclosure:** within **90 days**, sooner for
  high-severity issues

We will keep you updated as the investigation progresses, credit you in the
release notes if you wish, and publish a GitHub Security Advisory once a fix
ships.

Thank you for helping keep Aethex AI users safe.
