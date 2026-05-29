"""Create an agent, attach a knowledge-base doc, place a call.

Aethex AI — official SDK examples.

Uses the full :class:`aethexai.AethexAI` client (not the focused Kora
wrapper) so we can reach knowledge-base uploads and outbound calling from
the same object. End-to-end this example will:

  1. Create an agent with a full set of tunables (voice, language, dialect
     style, max duration, silence timeout, etc.).
  2. Upload a short text snippet to that agent's knowledge base.
  3. Update one of the agent's settings (``first_message``) post-create.
  4. Trigger an outbound call.
  5. Poll the call's status until it leaves the "queued"/"ringing" state
     or until ``MAX_POLL_SECONDS`` elapses.

Run::

    export AETHEX_API_KEY=ae_live_...
    export PHONE_NUMBER=+221700000000
    uv run python examples/agent_create_and_call.py

Required environment variables:

  * ``AETHEX_API_KEY`` — your Aethex API key.
  * ``PHONE_NUMBER`` — E.164 destination for the outbound call.
"""

from __future__ import annotations

import os
import sys
import time

from aethexai import AethexAI
from aethexai._generated.models.body_upload_knowledge_doc_api_v1_agents_agent_id_knowledge_base_post import (
    BodyUploadKnowledgeDocApiV1AgentsAgentIdKnowledgeBasePost,
)

MAX_POLL_SECONDS = 60
POLL_INTERVAL = 3
TERMINAL_STATUSES = {"completed", "failed", "no_answer", "busy", "cancelled"}


def main() -> int:
    api_key = os.getenv("AETHEX_API_KEY")
    if not api_key:
        print("error: set AETHEX_API_KEY before running this example", file=sys.stderr)
        return 1

    to_number = os.getenv("PHONE_NUMBER", "+221700000000")
    base_url = os.getenv("AETHEX_BASE_URL", "https://api.aethexai.com")

    with AethexAI(api_key=api_key, base_url=base_url) as client:
        # ── 1. Create the agent ──────────────────────────────────────────
        # All optional tunables are accepted as keyword arguments and
        # forwarded to the generated AgentCreate model via ``from_dict``.
        agent = client.create_agent(
            name="Aethex Banking Agent",
            system_prompt=(
                "You are a polite, concise banking assistant. "
                "Help callers check balances and reset their PIN."
            ),
            first_message="Bonjour, c'est Aethex.",
            voice_id="fatima",
            language="french",
            dialect_style="local",
            max_duration_seconds=300,
            silence_timeout_seconds=8,
        )
        print(f"Created agent: {agent['id']}")

        # ── 2. Upload a knowledge-base doc (text snippet) ────────────────
        # The multipart endpoint accepts either a raw file or an inline
        # ``text`` blob; we use the latter to keep the example dependency-
        # free.
        kb_body = BodyUploadKnowledgeDocApiV1AgentsAgentIdKnowledgeBasePost(
            text=(
                "Branch hours are Monday-Friday 8h-18h, Saturday 9h-13h. "
                "Customer support: +221 33 800 00 00."
            ),
            filename="branch-hours.txt",
        )
        doc = client.upload_knowledge_doc(agent["id"], body=kb_body)
        print(f"Uploaded knowledge doc: {doc.get('id', doc)}")

        # ── 3. Update the agent's first_message after the fact ───────────
        # Demonstrates PATCH semantics — only fields you pass get changed.
        updated = client.update_agent(
            agent["id"],
            first_message="Bonjour, Aethex Bank a votre service.",
        )
        print(f"Updated agent first_message; revision: {updated.get('id', 'ok')}")

        # ── 4. Place the outbound call ───────────────────────────────────
        call = client.trigger_call(agent_id=str(agent["id"]), to_number=to_number)
        print(f"Triggered call: {call['id']}")

        # ── 5. Poll for terminal status ──────────────────────────────────
        deadline = time.monotonic() + MAX_POLL_SECONDS
        last_status: str | None = None
        while time.monotonic() < deadline:
            status_resp = client.get_call_status(call["id"])
            status = status_resp.get("status") or status_resp.get("state", "unknown")
            if status != last_status:
                print(f"  call status: {status}")
                last_status = status
            if status in TERMINAL_STATUSES:
                break
            time.sleep(POLL_INTERVAL)
        else:
            print(f"  polling timed out after {MAX_POLL_SECONDS}s")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
