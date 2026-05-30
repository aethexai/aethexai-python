# Agents

Agents are the core primitive of the Aethex AI platform: a configured
combination of a **system prompt**, a **voice**, and a **language/dialect**
that can hold a real conversation over WebRTC, the telephone network, or any
audio surface you integrate.

This guide walks through the full agent lifecycle using the Python SDK's flat
client surface: every operation is a method on `AethexAI` — there are no
nested `client.agents.create(...)` namespaces.

## What an agent is

At minimum, an agent is defined by three things:

- **`name`** — a human-readable label, e.g. `"Front-desk receptionist"`.
- **`system_prompt`** — the natural-language instructions the underlying LLM
  receives on every turn. This is where you describe the agent's persona,
  goals, do's and don'ts, and any structured workflow.
- **`voice_id`** — the synthesised voice the agent speaks with. You can
  discover the available voices by calling `client.list_voices()`.

A handful of other knobs shape behaviour without changing the agent's
identity:

- **`first_message`** — what the agent says when a call connects.
- **`language`** — defaults to `"english"`. Set this when you want the agent
  to speak and understand a different language.
- **`dialect_style`** — `"formal"`, `"casual"`, or other styles supported by
  your account.
- **`temperature`**, **`max_tokens`**, **`max_duration_seconds`**,
  **`interruption_enabled`** — fine-grained controls over the LLM and the
  conversation pipeline.

The full list of fields lives in the generated `AgentCreate` model. The SDK
accepts them as keyword arguments to `create_agent` and forwards them to the
API.

## Creating an agent

```python
from aethexai import AethexAI

client = AethexAI(api_key="ak_live_...")

agent = client.create_agent(
    name="Front-desk receptionist",
    system_prompt=(
        "You are the receptionist for Acme Dental. "
        "Greet callers, answer basic questions, and book appointments."
    ),
    voice_id="vc_clear_female_en",
    first_message="Hi, you've reached Acme Dental — how can I help?",
    language="english",
    dialect_style="casual",
    temperature=0.4,
    interruption_enabled=True,
    max_duration_seconds=900,
)

print(agent["id"])
```

To list, fetch, update, duplicate, or delete agents, use the matching
flat methods:

```python
client.list_agents(limit=50)
client.get_agent(agent["id"])
client.update_agent(agent["id"], system_prompt="...updated prompt...")
client.duplicate_agent(agent["id"])
client.delete_agent(agent["id"])
```

## Managing the knowledge base

Each agent has its own knowledge base — a collection of documents the agent
can retrieve from during a conversation.

```python
# List what the agent already has
docs = client.list_knowledge_docs(agent["id"])

# Upload a document via multipart (e.g. a PDF or text file)
with open("policies.pdf", "rb") as fh:
    client.upload_knowledge_doc(agent["id"], body=fh)

# Or attach a previously presigned upload (see client.create_upload(...))
client.upload_knowledge_doc_by_upload(
    agent["id"],
    upload_id="up_...",
    filename="policies.pdf",
)

# Re-run extraction/embedding on a doc that already exists
client.process_knowledge_doc(agent["id"], doc_id="doc_...")

# Inspect the extracted text snippets
client.get_knowledge_texts(agent["id"])

# Ad-hoc query the knowledge base outside a conversation
client.query_knowledge_base(agent["id"], query="What is your refund policy?")

# Clean up
client.delete_knowledge_doc(agent["id"], doc_id="doc_...")
```

## Managing tools

Tools are server-side function definitions the LLM can invoke mid-conversation
(e.g. "book an appointment", "look up an order"). Each tool has a JSON-schema
parameter spec; the runtime calls your endpoint when the LLM decides to use
it, or it surfaces the call to your local code via the realtime channel.

```python
client.list_agent_tools(agent["id"])

client.add_agent_tool(
    agent["id"],
    name="book_appointment",
    description="Reserve a time slot for the caller.",
    tool_type="function",
    parameters_schema={
        "type": "object",
        "properties": {
            "patient_name": {"type": "string"},
            "iso_datetime": {"type": "string", "format": "date-time"},
        },
        "required": ["patient_name", "iso_datetime"],
    },
    endpoint_url="https://your-backend.example.com/book",
    headers={"Authorization": "Bearer ..."},
)

client.update_agent_tool(agent["id"], tool_id="tl_...", description="...")
client.delete_agent_tool(agent["id"], tool_id="tl_...")
```

## Triggering outbound calls

Once an agent exists, you can have it place a phone call:

```python
call = client.trigger_call(
    agent_id=agent["id"],
    to_number="+15551234567",
    from_number="+15557654321",  # optional — defaults to a number on file
    metadata={"customer_id": "cu_42"},
)

print(call["id"])
```

For high-volume scenarios use `client.batch_calls(...)` with a list of
recipients and inspect progress with `client.get_call_batch(batch_id)`.

## Live conversations

To talk to an agent in real time from a Python process — for example a
browser-less voice client, a phone-emulator bridge, or an automated test —
use the `aethexai.realtime.Conversation` helper.

```python
from aethexai import AsyncAethexAI
from aethexai.realtime import Conversation, ConversationCallbacks

async def main() -> None:
    client = AsyncAethexAI(api_key="ak_live_...")
    conv = Conversation(
        client,
        agent_id=agent["id"],
        callbacks=ConversationCallbacks(
            on_agent_audio=lambda pcm: speakers.write(pcm),
            on_agent_text=lambda text: print("agent:", text),
            on_user_transcript=lambda text: print("user:", text),
        ),
    )
    await conv.start()
    # ... feed conv.audio_input with microphone PCM frames ...
    await conv.end()
```

`Conversation` is only available when the `realtime` extra is installed:

```bash
pip install "aethexai[realtime]"
```

## End-to-end example

```python
from aethexai import AethexAI

client = AethexAI(api_key="ak_live_...")

# 1. Create the agent
agent = client.create_agent(
    name="Order-status bot",
    system_prompt=(
        "You help customers check the status of their orders. "
        "Use the lookup_order tool when given an order number."
    ),
    voice_id="vc_warm_neutral_en",
    first_message="Hi! What's your order number?",
)

# 2. Give it knowledge about the company
with open("returns_policy.md", "rb") as fh:
    client.upload_knowledge_doc(agent["id"], body=fh)

# 3. Give it a tool it can call
client.add_agent_tool(
    agent["id"],
    name="lookup_order",
    description="Fetch the status of a customer order by id.",
    parameters_schema={
        "type": "object",
        "properties": {"order_id": {"type": "string"}},
        "required": ["order_id"],
    },
    endpoint_url="https://your-backend.example.com/orders/status",
)

# 4. Call a customer back
client.trigger_call(
    agent_id=agent["id"],
    to_number="+15551234567",
    metadata={"order_id": "ord_98123"},
)
```

That's the full loop: configure → enrich → connect.

For the reference list of every keyword argument, see the generated
`AgentCreate`, `AgentToolCreate`, and `CallCreate` models in
`src/aethexai/_generated/models/`, or browse the hosted reference at
<https://docs.aethexai.com/agents>.
