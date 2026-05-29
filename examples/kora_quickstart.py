"""Kora quickstart — create an agent and trigger an outbound call.

Aethex AI — official SDK examples.

This is the minimal "hello world" for the voice-only Kora client. It:

  1. Creates a French-language banking agent with the ``fatima`` voice.
  2. Triggers an outbound call from that agent to ``PHONE_NUMBER``.

Run::

    export AETHEX_API_KEY=ae_live_...
    export PHONE_NUMBER=+221700000000
    uv run python examples/kora_quickstart.py

Required environment variables:

  * ``AETHEX_API_KEY`` — your Aethex API key (starts with ``ae_live_`` or ``ae_test_``).
  * ``PHONE_NUMBER`` — E.164 destination, e.g. ``+221700000000``.
"""

from __future__ import annotations

import os
import sys

from aethexai import Kora


def main() -> int:
    api_key = os.getenv("AETHEX_API_KEY")
    if not api_key:
        print("error: set AETHEX_API_KEY before running this example", file=sys.stderr)
        return 1

    # PHONE_NUMBER falls back to a Senegal-region placeholder so a bare
    # `python examples/kora_quickstart.py` still has a sensible default;
    # the real call will only succeed if you override it.
    to_number = os.getenv("PHONE_NUMBER", "+221700000000")
    base_url = os.getenv("AETHEX_BASE_URL", "https://api.aethexai.com")

    client = Kora(base_url, api_key)

    agent = client.create_agent(
        name="Aethex Agent",
        system_prompt="You are a banking assistant.",
        first_message="Bonjour!",
        voice_id="fatima",
        language="french",
        dialect_style="local",
    )
    print(f"Created agent: {agent['id']}")

    call = client.trigger_call(agent["id"], to_number=to_number)
    print(f"Started call: {call['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
