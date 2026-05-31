---
name: agents-and-knowledge-base
description: Create, fetch, and delete AethexAI voice agents and manage an agent's knowledge base (RAG) with the sync AethexAI client. Use when you need to "create an agent", "get/delete an agent", "upload a document to an agent's knowledge base", "list knowledge docs", "query the knowledge base", run "RAG retrieval" against an agent, or "delete a knowledge doc". Also covers the throwaway-agent self-cleanup pattern for safely exercising KB CRUD against a live tenant.
tools: Bash, Read, Edit, Write
---

# Agents & Knowledge Base

Manage agents and their knowledge base (KB) through the synchronous `AethexAI` client
(`src/aethexai/client.py`). Every method below is verified against current `main` and the
test suite. The KB endpoints back retrieval-augmented generation (RAG): you upload docs,
they get indexed into text chunks, and `query_knowledge_base` returns the most relevant
chunks with a relevance score.

## When to use this skill

- Creating an agent and reading back its `id`.
- Fetching or deleting an agent.
- Uploading a file (or raw text) into an agent's knowledge base.
- Listing KB docs, inspecting indexed text, or querying the KB (RAG).
- Deleting a KB doc.
- Exercising KB CRUD safely against a live tenant via a disposable agent.

## Client setup

```python
from aethexai import AethexAI

# Pass api_key= explicitly, or rely on the AETHEX_API_KEY env var.
client = AethexAI(api_key="ak_live_...")
# base_url defaults to https://api.aethexai.com
```

## Agent CRUD

### create_agent — returns a typed `AgentResponse`

`create_agent(**fields)` builds an `AgentCreate` body. The three required fields are
`name`, `system_prompt`, and `voice_id`; `language` and many tuning fields are optional
(default `language="english"`).

It returns a typed **`AgentResponse`**, so `agent.id` works directly:

```python
agent = client.create_agent(
    name="Support Bot",
    system_prompt="You are a helpful support agent.",
    voice_id="fatima",
    language="english",
)
print(agent.id)    # attribute access works — AgentResponse, not a dict
print(agent.name)  # "Support Bot"
```

> IMPORTANT: Always use attribute access (`agent.id`), never subscripting (`agent["id"]`).
> An older note claimed `create_agent` returned a raw dict — that is **stale**. It now
> returns a typed `AgentResponse` on both 201 and 200 responses, enforced by
> `tests/test_typed_agent_responses.py`.

### get_agent / delete_agent

```python
from uuid import UUID

agent = client.get_agent(agent.id)           # accepts str or UUID; returns AgentResponse
client.delete_agent(agent.id)                # accepts str or UUID
```

After deletion, fetching the same agent raises `NotFoundError`:

```python
from aethexai import NotFoundError

client.delete_agent(agent.id)
try:
    client.get_agent(agent.id)
except NotFoundError:
    print("agent is gone")  # expected after delete
```

## Knowledge base (RAG)

All KB methods take the agent id as the first positional argument (str or UUID).

### upload_knowledge_doc — multipart file upload

`upload_knowledge_doc(agent_id, *, body=...)` takes a multipart body. Construct it with
the generated body model and a `File`, both from `aethexai._generated.types` /
`aethexai._generated.models`. The body model exposes `file`, `filename`, and `text`
fields — pass a `File` to upload bytes, or pass `text=` to index a raw string.

```python
from io import BytesIO

from aethexai._generated.types import File
from aethexai._generated.models.body_upload_knowledge_doc_api_v1_agents_agent_id_knowledge_base_post import (
    BodyUploadKnowledgeDocApiV1AgentsAgentIdKnowledgeBasePost as UploadBody,
)

content = b"Acme Corp refunds are processed within 5 business days."
body = UploadBody(
    file=File(
        payload=BytesIO(content),
        file_name="refunds.txt",
        mime_type="text/plain",
    ),
)
doc = client.upload_knowledge_doc(agent.id, body=body)  # parsed JSON dict, not a typed model
doc_id = doc["id"]     # the doc id used for delete (subscript — the response is a dict)
print(doc_id)
print(doc["status"])   # e.g. "processing" right after upload, "completed" once indexed
```

### list_knowledge_docs / get_knowledge_texts

```python
docs = client.list_knowledge_docs(agent.id)    # parsed JSON list of docs (status -> "completed")
texts = client.get_knowledge_texts(agent.id)   # indexed text snippets for the agent
print(docs)
print(texts)  # count grows to >=1 once a doc is indexed
```

Indexing is asynchronous: a freshly uploaded doc starts at `status="processing"` and
flips to `"completed"` within a couple of polls. Poll `list_knowledge_docs` (or check
`doc.status`) until it reports `"completed"` before querying.

### query_knowledge_base — RAG retrieval

`query_knowledge_base(agent_id, query=..., top_k=...)` builds a `KnowledgeQueryRequest`
(`top_k` defaults to 3). It returns a `KnowledgeQueryResponse` with `.query` and a
`.results` list; each result has a relevance `.score`, the matching `.text`, and a
`.source`.

```python
hits = client.query_knowledge_base(agent.id, query="How long do refunds take?", top_k=2)
for r in hits.results:
    print(r.score, r.text)  # e.g. 0.0328  "Acme Corp refunds are processed within 5 business days."
```

### delete_knowledge_doc

```python
client.delete_knowledge_doc(agent.id, doc_id)  # doc_id == doc["id"]; both args accept str or UUID
```

## Throwaway-agent self-cleanup pattern

When exercising KB CRUD against a live tenant, do it on a **disposable** agent and delete
it in the same run so no residue is left behind. Because `create_agent` now returns a
typed `AgentResponse`, you can capture `agent.id` immediately for cleanup — the old
"dict leak" footgun (where `agent.id` raised before cleanup could run) is resolved.

```python
import time
from io import BytesIO

from aethexai import AethexAI, NotFoundError
from aethexai._generated.types import File
from aethexai._generated.models.body_upload_knowledge_doc_api_v1_agents_agent_id_knowledge_base_post import (
    BodyUploadKnowledgeDocApiV1AgentsAgentIdKnowledgeBasePost as UploadBody,
)

client = AethexAI(api_key="ak_live_...")

agent = client.create_agent(
    name="SDK Test Agent (delete me)",
    system_prompt="Throwaway agent for KB testing.",
    voice_id="fatima",
)
try:
    body = UploadBody(
        file=File(
            payload=BytesIO(b"Acme Corp refunds are processed within 5 business days."),
            file_name="refunds.txt",
            mime_type="text/plain",
        ),
    )
    doc = client.upload_knowledge_doc(agent.id, body=body)  # parsed JSON dict
    doc_id = doc["id"]

    # Wait for indexing to finish (usually completes within a couple of polls).
    for _ in range(10):
        docs = client.list_knowledge_docs(agent.id)
        items = docs["documents"] if isinstance(docs, dict) else docs
        if items and items[0]["status"] == "completed":
            break
        time.sleep(2)

    print(client.get_knowledge_texts(agent.id))
    hits = client.query_knowledge_base(agent.id, query="refund time?", top_k=2)
    for r in hits.results:
        print(r.score, r.text)

    client.delete_knowledge_doc(agent.id, doc_id)
finally:
    # Always clean up the throwaway agent, even if the body above raised.
    client.delete_agent(agent.id)

# Verify cleanup: the agent must be gone.
try:
    client.get_agent(agent.id)
    raise AssertionError("agent was not deleted")
except NotFoundError:
    pass  # expected
```

## Gotchas

- `create_agent` returns a typed `AgentResponse` (use `agent.id`, not `agent["id"]`).
- The uploaded doc's id is `doc["id"]` (the upload response is a parsed JSON dict, not a
  typed model); pass it as the second positional arg to `delete_knowledge_doc`.
- KB indexing is async — wait for `status="completed"` before querying, or RAG results
  may be empty.
- `list_knowledge_docs`, `get_knowledge_texts`, and `upload_knowledge_doc` return parsed
  JSON payloads (not typed models); only `query_knowledge_base` returns a typed model
  (`KnowledgeQueryResponse`).
- Use the throwaway-agent pattern with a `try/finally` so a live tenant is never left
  with stray test agents or docs.
- **Required-field validation fails fast, client-side.** Omitting a required field
  (e.g. `voice_id` on `create_agent`, or `query` on `query_knowledge_base`) raises
  `aethexai.ValidationError` *before* any HTTP request, with `.response` listing every
  missing field — it is not a bare `KeyError`.
- **RAG scores are small relative values.** A strong hit scored ~0.03 in live testing,
  so rank results by `.score` and take the top ones — don't apply a high absolute
  threshold (e.g. `> 0.5`) or you'll discard good matches.

See CLAUDE.md for repo-working context (install, tests, lint/types, env vars).
