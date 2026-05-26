"""Synchronous Aethex AI client with a flat-method API.

This module exposes ``AethexAI``, a thin, ergonomic wrapper around the
generated OpenAPI client at ``aethexai._generated``. Every user-facing
operation in the platform is exposed as a top-level method on the
client — no nested ``client.agents.create(...)``-style namespaces.

Example::

    from aethexai import AethexAI

    client = AethexAI(api_key="ak_live_...")
    agent = client.create_agent(name="Bot", system_prompt="You are helpful.")
    print(agent)
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from typing import Any
from uuid import UUID

import httpx

from aethexai._body import build_body
from aethexai._exceptions import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    _map_status_to_exception,
)
from aethexai._generated.client import AuthenticatedClient
from aethexai._generated.types import UNSET, Unset

_DEFAULT_BASE_URL = "https://api.aethexai.com"


class AethexAI:
    """Synchronous Aethex AI client.

    Args:
        api_key: Aethex API key. Falls back to the ``AETHEX_API_KEY`` env var.
        base_url: API base URL. Defaults to https://api.aethexai.com.
        timeout: Per-request timeout in seconds.
        max_retries: Number of HTTP-level retries (wired via httpx transport).
        httpx_client: Optional pre-built ``httpx.Client`` to use as the transport.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 2,
        httpx_client: httpx.Client | None = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("AETHEX_API_KEY", "")
        if not resolved_key:
            raise AuthenticationError(
                "API key is required. Pass api_key= or set the AETHEX_API_KEY env var.",
                status_code=401,
            )
        # NOTE: the API key is intentionally NOT stored as an instance attribute.
        # It lives only inside ``self._client`` (the generated ``AuthenticatedClient``),
        # which suppresses it from ``repr()``. Anything that stores the raw key
        # on ``self`` would leak via ``vars(client)`` / ``client.__dict__``.
        # See finding A.5 in docs/audits/pre-launch-2026-05-17.md.
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

        httpx_args: dict[str, Any] = {
            "transport": httpx.HTTPTransport(retries=max_retries),
        }
        self._client = AuthenticatedClient(
            base_url=self._base_url,
            token=resolved_key,
            auth_header_name="X-API-Key",
            prefix="",
            timeout=httpx.Timeout(timeout),
            httpx_args=httpx_args,
        )
        if httpx_client is not None:
            self._client.set_httpx_client(httpx_client)

    # ── Lifecycle ──────────────────────────────────────────────────────

    def __repr__(self) -> str:
        # Explicit safe repr — never include any field that could carry the
        # API key (directly or by reference). The default object repr would
        # be fine today, but a future ``self.foo = secret`` would silently
        # leak via the default ``str(vars(self))``. Keep this tight.
        return f"{type(self).__name__}(base_url={self._base_url!r}, timeout={self._timeout!r})"

    def close(self) -> None:
        """Close the underlying HTTP client."""
        inner = self._client.get_httpx_client()
        inner.close()

    def __enter__(self) -> AethexAI:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    # ── Internal request runner ────────────────────────────────────────

    def _call(self, op_func: Any, *args: Any, **kwargs: Any) -> Any:
        """Run a generated ``_detailed`` op, raise on non-2xx, return parsed result.

        Every wrapper method funnels through here so that the SDK consistently
        raises a typed exception (mapped via :func:`_map_status_to_exception`)
        instead of silently returning ``None`` on HTTP errors.
        """
        try:
            response = op_func(*args, client=self._client, **kwargs)
        except httpx.TimeoutException as exc:
            raise APITimeoutError() from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(cause=exc) from exc
        status = int(response.status_code)
        if 200 <= status < 300:
            return response.parsed
        raise _map_status_to_exception(status, response.content, response.headers)

    def _call_bytes(self, op_func: Any, *args: Any, **kwargs: Any) -> bytes:
        """Variant of :meth:`_call` that returns raw response bytes on 2xx.

        Used for endpoints whose response body is binary content (audio,
        files) rather than JSON.
        """
        try:
            response = op_func(*args, client=self._client, **kwargs)
        except httpx.TimeoutException as exc:
            raise APITimeoutError() from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(cause=exc) from exc
        status = int(response.status_code)
        if 200 <= status < 300:
            content: bytes = response.content
            return content
        raise _map_status_to_exception(status, response.content, response.headers)

    # ─── agents ────────────────────────────────────────────────────────

    def list_agents(self, *, offset: int | Unset = 0, limit: int | Unset = 50) -> Any:
        """List agents. See https://docs.aethexai.com/agents."""
        from aethexai._generated.api.agents import list_agents_api_v1_agents_get as _op

        return self._call(_op.sync_detailed, offset=offset, limit=limit)

    def create_agent(self, **fields: Any) -> Any:
        """Create a new agent. See https://docs.aethexai.com/agents."""
        from aethexai._generated.api.agents import create_agent_api_v1_agents_post as _op
        from aethexai._generated.models.agent_create import AgentCreate

        return self._call(_op.sync_detailed, body=build_body(AgentCreate, fields))

    def get_agent(self, agent_id: str | UUID) -> Any:
        """Retrieve an agent by id. See https://docs.aethexai.com/agents."""
        from aethexai._generated.api.agents import get_agent_api_v1_agents_agent_id_get as _op

        return self._call(_op.sync_detailed, UUID(str(agent_id)))

    def update_agent(self, agent_id: str | UUID, **fields: Any) -> Any:
        """Update an existing agent. See https://docs.aethexai.com/agents."""
        from aethexai._generated.api.agents import update_agent_api_v1_agents_agent_id_patch as _op
        from aethexai._generated.models.agent_update import AgentUpdate

        return self._call(
            _op.sync_detailed, UUID(str(agent_id)), body=build_body(AgentUpdate, fields)
        )

    def delete_agent(self, agent_id: str | UUID) -> Any:
        """Delete an agent. See https://docs.aethexai.com/agents."""
        from aethexai._generated.api.agents import delete_agent_api_v1_agents_agent_id_delete as _op

        return self._call(_op.sync_detailed, UUID(str(agent_id)))

    def duplicate_agent(self, agent_id: str | UUID) -> Any:
        """Duplicate an existing agent. See https://docs.aethexai.com/agents."""
        from aethexai._generated.api.agents import (
            duplicate_agent_api_v1_agents_agent_id_duplicate_post as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(agent_id)))

    def list_agent_tools(self, agent_id: str | UUID) -> Any:
        """List tools for an agent. See https://docs.aethexai.com/agents."""
        from aethexai._generated.api.agents import (
            list_tools_api_v1_agents_agent_id_tools_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(agent_id)))

    def add_agent_tool(self, agent_id: str | UUID, **fields: Any) -> Any:
        """Attach a tool to an agent. See https://docs.aethexai.com/agents."""
        from aethexai._generated.api.agents import add_tool_api_v1_agents_agent_id_tools_post as _op
        from aethexai._generated.models.agent_tool_create import AgentToolCreate

        return self._call(
            _op.sync_detailed, UUID(str(agent_id)), body=build_body(AgentToolCreate, fields)
        )

    def update_agent_tool(self, agent_id: str | UUID, tool_id: str | UUID, **fields: Any) -> Any:
        """Update an agent tool. See https://docs.aethexai.com/agents."""
        from aethexai._generated.api.agents import (
            update_tool_api_v1_agents_agent_id_tools_tool_id_patch as _op,
        )
        from aethexai._generated.models.agent_tool_update import AgentToolUpdate

        return self._call(
            _op.sync_detailed,
            UUID(str(agent_id)),
            UUID(str(tool_id)),
            body=build_body(AgentToolUpdate, fields),
        )

    def delete_agent_tool(self, agent_id: str | UUID, tool_id: str | UUID) -> Any:
        """Detach a tool from an agent. See https://docs.aethexai.com/agents."""
        from aethexai._generated.api.agents import (
            delete_tool_api_v1_agents_agent_id_tools_tool_id_delete as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(agent_id)), UUID(str(tool_id)))

    def list_knowledge_docs(self, agent_id: str | UUID) -> Any:
        """List knowledge-base documents for an agent. See https://docs.aethexai.com/knowledge-base."""
        from aethexai._generated.api.agents import (
            list_knowledge_docs_api_v1_agents_agent_id_knowledge_base_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(agent_id)))

    def upload_knowledge_doc(self, agent_id: str | UUID, *, body: Any | Unset = UNSET) -> Any:
        """Upload a knowledge-base document (multipart). See https://docs.aethexai.com/knowledge-base."""
        from aethexai._generated.api.agents import (
            upload_knowledge_doc_api_v1_agents_agent_id_knowledge_base_post as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(agent_id)), body=body)

    def upload_knowledge_doc_by_upload(self, agent_id: str | UUID, **fields: Any) -> Any:
        """Attach a previously presigned upload as a knowledge-base doc. See https://docs.aethexai.com/knowledge-base."""
        from aethexai._generated.api.agents import (
            upload_knowledge_doc_by_upload_api_v1_agents_agent_id_knowledge_base_by_upload_post as _op,
        )
        from aethexai._generated.models.knowledge_doc_by_upload_request import (
            KnowledgeDocByUploadRequest,
        )

        return self._call(
            _op.sync_detailed,
            UUID(str(agent_id)),
            body=build_body(KnowledgeDocByUploadRequest, fields),
        )

    def delete_knowledge_doc(self, agent_id: str | UUID, doc_id: str | UUID) -> Any:
        """Delete a knowledge-base document. See https://docs.aethexai.com/knowledge-base."""
        from aethexai._generated.api.agents import (
            delete_knowledge_doc_api_v1_agents_agent_id_knowledge_base_doc_id_delete as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(agent_id)), UUID(str(doc_id)))

    def process_knowledge_doc(self, agent_id: str | UUID, doc_id: str | UUID) -> Any:
        """Re-process a knowledge-base document. See https://docs.aethexai.com/knowledge-base."""
        from aethexai._generated.api.agents import (
            process_knowledge_doc_api_v1_agents_agent_id_knowledge_base_doc_id_process_post as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(agent_id)), UUID(str(doc_id)))

    def get_knowledge_texts(self, agent_id: str | UUID) -> Any:
        """Fetch raw knowledge-base text snippets for an agent. See https://docs.aethexai.com/knowledge-base."""
        from aethexai._generated.api.agents import (
            get_knowledge_texts_api_v1_agents_agent_id_knowledge_base_texts_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(agent_id)))

    def query_knowledge_base(self, agent_id: str | UUID, **fields: Any) -> Any:
        """Query an agent's knowledge base. See https://docs.aethexai.com/knowledge-base."""
        from aethexai._generated.api.agents import (
            query_knowledge_base_api_v1_agents_agent_id_knowledge_base_query_post as _op,
        )
        from aethexai._generated.models.knowledge_query_request import KnowledgeQueryRequest

        return self._call(
            _op.sync_detailed,
            UUID(str(agent_id)),
            body=build_body(KnowledgeQueryRequest, fields),
        )

    # ─── api_keys ──────────────────────────────────────────────────────

    def list_api_keys(self) -> Any:
        """List API keys. See https://docs.aethexai.com/api-keys."""
        from aethexai._generated.api.api_keys import list_api_keys_api_v1_api_keys_get as _op

        return self._call(_op.sync_detailed)

    def create_api_key(self, **fields: Any) -> Any:
        """Create a new API key. See https://docs.aethexai.com/api-keys."""
        from aethexai._generated.api.api_keys import create_api_key_api_v1_api_keys_post as _op
        from aethexai._generated.models.api_key_create import APIKeyCreate

        return self._call(_op.sync_detailed, body=build_body(APIKeyCreate, fields))

    def revoke_api_key(self, key_id: str | UUID) -> Any:
        """Revoke an API key. See https://docs.aethexai.com/api-keys."""
        from aethexai._generated.api.api_keys import (
            revoke_api_key_api_v1_api_keys_key_id_delete as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(key_id)))

    def rotate_api_key(self, key_id: str | UUID) -> Any:
        """Rotate an API key. See https://docs.aethexai.com/api-keys."""
        from aethexai._generated.api.api_keys import (
            rotate_api_key_api_v1_api_keys_key_id_rotate_post as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(key_id)))

    # NOTE (2026-05-17, audit finding A.1): the 8 billing methods that used
    # to live here (get_balance, list_plans, select_plan, list_invoices,
    # list_transactions, list_payment_methods,
    # create_payment_method_setup_intent, detach_payment_method) were
    # removed because their server routes require a developer JWT
    # (``Authorization: Bearer <jwt>``), and ``AethexAI`` only sends
    # ``X-API-Key``. Every call returned 401 against the live server.
    # They are now available on ``aethexai.DeveloperClient`` /
    # ``AsyncDeveloperClient`` with proper JWT auth + token refresh.

    # ─── calls ─────────────────────────────────────────────────────────

    def list_calls(
        self,
        *,
        status: str | None | Unset = UNSET,
        direction: Any | None | Unset = UNSET,
        offset: int | Unset = 0,
        limit: int | Unset = 50,
    ) -> Any:
        """List calls. See https://docs.aethexai.com/calls."""
        from aethexai._generated.api.calls import list_calls_api_v1_calls_get as _op

        return self._call(
            _op.sync_detailed, status=status, direction=direction, offset=offset, limit=limit
        )

    def create_call_record(self, **fields: Any) -> Any:
        """Create a call record. See https://docs.aethexai.com/calls."""
        from aethexai._generated.api.calls import create_call_record_api_v1_calls_post as _op
        from aethexai._generated.models.call_record_create import CallRecordCreate

        return self._call(_op.sync_detailed, body=build_body(CallRecordCreate, fields))

    def get_call(self, call_id: str | UUID) -> Any:
        """Retrieve a call by id. See https://docs.aethexai.com/calls."""
        from aethexai._generated.api.calls import get_call_api_v1_calls_call_id_get as _op

        return self._call(_op.sync_detailed, UUID(str(call_id)))

    def get_call_status(self, call_id: str | UUID) -> Any:
        """Get a call's current status. See https://docs.aethexai.com/calls."""
        from aethexai._generated.api.calls import (
            get_call_status_api_v1_calls_call_id_status_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(call_id)))

    def trigger_call(self, **fields: Any) -> Any:
        """Place an outbound call. See https://docs.aethexai.com/calls."""
        from aethexai._generated.api.calls import trigger_call_api_v1_calls_trigger_post as _op
        from aethexai._generated.models.call_create import CallCreate

        return self._call(_op.sync_detailed, body=build_body(CallCreate, fields))

    def batch_calls(self, **fields: Any) -> Any:
        """Trigger a batch of outbound calls. See https://docs.aethexai.com/calls."""
        from aethexai._generated.api.calls import batch_calls_api_v1_calls_batch_post as _op
        from aethexai._generated.models.batch_call_create import BatchCallCreate

        return self._call(_op.sync_detailed, body=build_body(BatchCallCreate, fields))

    def get_call_batch(self, batch_id: str | UUID) -> Any:
        """Retrieve a call batch by id. See https://docs.aethexai.com/calls."""
        from aethexai._generated.api.calls import get_batch_api_v1_calls_batch_batch_id_get as _op

        return self._call(_op.sync_detailed, UUID(str(batch_id)))

    # ─── conversation (live session control) ───────────────────────────

    def conversation_connect(self, **fields: Any) -> Any:
        """Establish a new conversation session. See https://docs.aethexai.com/conversation."""
        from aethexai._generated.api.conversation import (
            connect_api_v1_conversation_connect_post as _op,
        )
        from aethexai._generated.models.connect_request import ConnectRequest

        return self._call(_op.sync_detailed, body=build_body(ConnectRequest, fields))

    def end_conversation_session(self, session_id: str) -> Any:
        """End a live conversation session. See https://docs.aethexai.com/conversation."""
        from aethexai._generated.api.conversation import (
            end_session_api_v1_conversation_session_id_end_post as _op,
        )

        return self._call(_op.sync_detailed, session_id)

    def get_conversation_session_status(self, session_id: str) -> Any:
        """Get a conversation session's status. See https://docs.aethexai.com/conversation."""
        from aethexai._generated.api.conversation import (
            get_session_status_api_v1_conversation_session_id_status_get as _op,
        )

        return self._call(_op.sync_detailed, session_id)

    def send_ice_candidate(self, session_id: str, **fields: Any) -> Any:
        """Send an ICE candidate for a WebRTC session. See https://docs.aethexai.com/conversation."""
        from aethexai._generated.api.conversation import (
            ice_candidate_api_v1_conversation_session_id_ice_patch as _op,
        )
        from aethexai._generated.models.small_web_rtc_patch_request import SmallWebRTCPatchRequest

        return self._call(
            _op.sync_detailed, session_id, body=build_body(SmallWebRTCPatchRequest, fields)
        )

    def send_offer(self, session_id: str, **fields: Any) -> Any:
        """Send an SDP offer for a WebRTC session. See https://docs.aethexai.com/conversation."""
        from aethexai._generated.api.conversation import (
            offer_api_v1_conversation_session_id_offer_post as _op,
        )
        from aethexai._generated.models.small_web_rtc_request import SmallWebRTCRequest

        return self._call(
            _op.sync_detailed, session_id, body=build_body(SmallWebRTCRequest, fields)
        )

    def send_tool_result(self, session_id: str, **fields: Any) -> Any:
        """Return a tool-call result to a live conversation. See https://docs.aethexai.com/conversation."""
        from aethexai._generated.api.conversation import (
            tool_result_api_v1_conversation_session_id_tool_result_post as _op,
        )
        from aethexai._generated.models.tool_result_request import ToolResultRequest

        return self._call(_op.sync_detailed, session_id, body=build_body(ToolResultRequest, fields))

    # ─── conversations (historical) ────────────────────────────────────

    def list_conversations(self, *, offset: int | Unset = 0, limit: int | Unset = 50) -> Any:
        """List conversations. See https://docs.aethexai.com/conversations."""
        from aethexai._generated.api.conversations import (
            list_conversations_api_v1_conversations_get as _op,
        )

        return self._call(_op.sync_detailed, offset=offset, limit=limit)

    def get_conversation(self, conversation_id: str | UUID) -> Any:
        """Retrieve a conversation by id. See https://docs.aethexai.com/conversations."""
        from aethexai._generated.api.conversations import (
            get_conversation_api_v1_conversations_conversation_id_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(conversation_id)))

    def get_conversation_diagnostics(
        self,
        conversation_id: str | UUID,
        *,
        limit: int | Unset = 500,
        event_type: str | None | Unset = UNSET,
        stage: str | None | Unset = UNSET,
        severity: str | None | Unset = UNSET,
    ) -> Any:
        """Fetch diagnostics events for a conversation. See https://docs.aethexai.com/conversations."""
        from aethexai._generated.api.conversations import (
            get_conversation_diagnostics_api_v1_conversations_conversation_id_diagnostics_get as _op,
        )

        return self._call(
            _op.sync_detailed,
            UUID(str(conversation_id)),
            limit=limit,
            event_type=event_type,
            stage=stage,
            severity=severity,
        )

    def get_transcript(self, conversation_id: str | UUID) -> Any:
        """Fetch a conversation transcript. See https://docs.aethexai.com/conversations."""
        from aethexai._generated.api.conversations import (
            get_transcript_api_v1_conversations_conversation_id_transcript_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(conversation_id)))

    def get_audio(self, conversation_id: str | UUID) -> Any:
        """Get audio metadata for a conversation. See https://docs.aethexai.com/conversations."""
        from aethexai._generated.api.conversations import (
            get_audio_api_v1_conversations_conversation_id_audio_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(conversation_id)))

    def stream_audio(
        self,
        conversation_id: str | UUID,
        *,
        token: str | None | Unset = UNSET,
        range_: str | None | Unset = UNSET,
    ) -> Any:
        """Stream raw conversation audio (WAV). See https://docs.aethexai.com/conversations."""
        from aethexai._generated.api.conversations import (
            stream_audio_api_v1_conversations_conversation_id_audio_wav_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(conversation_id)), token=token, range_=range_)

    def revoke_audio_token(self, conversation_id: str | UUID, **fields: Any) -> Any:
        """Revoke an audio playback token. See https://docs.aethexai.com/conversations."""
        from aethexai._generated.api.conversations import (
            revoke_audio_token_api_v1_conversations_conversation_id_audio_revoke_post as _op,
        )
        from aethexai._generated.models.audio_revoke_body import AudioRevokeBody

        return self._call(
            _op.sync_detailed, UUID(str(conversation_id)), body=build_body(AudioRevokeBody, fields)
        )

    def submit_feedback(self, conversation_id: str | UUID, **fields: Any) -> Any:
        """Submit feedback on a conversation. See https://docs.aethexai.com/conversations."""
        from aethexai._generated.api.conversations import (
            submit_feedback_api_v1_conversations_conversation_id_feedback_post as _op,
        )
        from aethexai._generated.models.conversation_feedback import ConversationFeedback

        return self._call(
            _op.sync_detailed,
            UUID(str(conversation_id)),
            body=build_body(ConversationFeedback, fields),
        )

    def search_conversations(self, q: str, *, limit: int | Unset = 20) -> Any:
        """Search conversations. See https://docs.aethexai.com/conversations."""
        from aethexai._generated.api.conversations import (
            search_conversations_api_v1_conversations_search_get as _op,
        )

        return self._call(_op.sync_detailed, q=q, limit=limit)

    # ─── models ────────────────────────────────────────────────────────

    def list_models(self, *, include_unavailable: bool | Unset = False) -> Any:
        """List available LLM and voice models. See https://docs.aethexai.com/models."""
        from aethexai._generated.api.models import list_models_api_v1_models_get as _op

        return self._call(_op.sync_detailed, include_unavailable=include_unavailable)

    # ─── phone_numbers ─────────────────────────────────────────────────

    def list_phone_numbers(self, *, offset: int | Unset = 0, limit: int | Unset = 50) -> Any:
        """List provisioned phone numbers. See https://docs.aethexai.com/phone-numbers."""
        from aethexai._generated.api.phone_numbers import (
            list_phone_numbers_api_v1_phone_numbers_get as _op,
        )

        return self._call(_op.sync_detailed, offset=offset, limit=limit)

    def get_phone_number(self, pn_id: str | UUID) -> Any:
        """Retrieve a phone number by id. See https://docs.aethexai.com/phone-numbers."""
        from aethexai._generated.api.phone_numbers import (
            get_phone_number_api_v1_phone_numbers_pn_id_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(pn_id)))

    def update_phone_number(self, pn_id: str | UUID, **fields: Any) -> Any:
        """Update a phone number's configuration. See https://docs.aethexai.com/phone-numbers."""
        from aethexai._generated.api.phone_numbers import (
            update_phone_number_api_v1_phone_numbers_pn_id_patch as _op,
        )
        from aethexai._generated.models.phone_number_update import PhoneNumberUpdate

        return self._call(
            _op.sync_detailed, UUID(str(pn_id)), body=build_body(PhoneNumberUpdate, fields)
        )

    def release_phone_number(self, pn_id: str | UUID) -> Any:
        """Release (deprovision) a phone number. See https://docs.aethexai.com/phone-numbers."""
        from aethexai._generated.api.phone_numbers import (
            release_phone_number_api_v1_phone_numbers_pn_id_delete as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(pn_id)))

    def set_phone_number_routing(self, pn_id: str | UUID, **fields: Any) -> Any:
        """Configure inbound routing for a phone number. See https://docs.aethexai.com/phone-numbers."""
        from aethexai._generated.api.phone_numbers import (
            set_routing_api_v1_phone_numbers_pn_id_routing_post as _op,
        )
        from aethexai._generated.models.inbound_routing_config import InboundRoutingConfig

        return self._call(
            _op.sync_detailed,
            UUID(str(pn_id)),
            body=build_body(InboundRoutingConfig, fields),
        )

    def register_sip_phone_number(self, **fields: Any) -> Any:
        """Register an externally-hosted SIP phone number. See https://docs.aethexai.com/phone-numbers."""
        from aethexai._generated.api.phone_numbers import (
            register_sip_api_v1_phone_numbers_sip_register_post as _op,
        )
        from aethexai._generated.models.sip_register_request import SipRegisterRequest

        return self._call(_op.sync_detailed, body=build_body(SipRegisterRequest, fields))

    def register_twilio_phone_number(self, **fields: Any) -> Any:
        """Register a Twilio-managed phone number. See https://docs.aethexai.com/phone-numbers."""
        from aethexai._generated.api.phone_numbers import (
            register_twilio_api_v1_phone_numbers_twilio_register_post as _op,
        )
        from aethexai._generated.models.twilio_register_request import TwilioRegisterRequest

        return self._call(_op.sync_detailed, body=build_body(TwilioRegisterRequest, fields))

    # ─── twilio accounts ──────────────────────────────────────────────

    def register_twilio_account(self, **fields: Any) -> Any:
        """Register a Bring-Your-Own Twilio account."""
        from aethexai._generated.api.twilio_accounts import (
            register_twilio_account_api_v1_twilio_accounts_post as _op,
        )
        from aethexai._generated.models.twilio_account_create import TwilioAccountCreate

        return self._call(_op.sync_detailed, body=build_body(TwilioAccountCreate, fields))

    def list_twilio_accounts(self, *, offset: int | Unset = 0, limit: int | Unset = 50) -> Any:
        """List Twilio accounts available to the tenant."""
        from aethexai._generated.api.twilio_accounts import (
            list_twilio_accounts_api_v1_twilio_accounts_get as _op,
        )

        return self._call(_op.sync_detailed, offset=offset, limit=limit)

    def get_twilio_account(self, account_id: str | UUID) -> Any:
        """Retrieve a Twilio account by id."""
        from aethexai._generated.api.twilio_accounts import (
            get_twilio_account_api_v1_twilio_accounts_account_id_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(account_id)))

    def release_twilio_account(self, account_id: str | UUID) -> Any:
        """Release a tenant-owned Twilio account."""
        from aethexai._generated.api.twilio_accounts import (
            release_twilio_account_api_v1_twilio_accounts_account_id_delete as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(account_id)))

    # ─── recordings ────────────────────────────────────────────────────

    def list_recordings(self, *, offset: int | Unset = 0, limit: int | Unset = 50) -> Any:
        """List recordings. See https://docs.aethexai.com/recordings."""
        from aethexai._generated.api.recordings import list_recordings_api_v1_recordings_get as _op

        return self._call(_op.sync_detailed, offset=offset, limit=limit)

    def get_recording(self, recording_id: str | UUID) -> Any:
        """Retrieve a recording by id. See https://docs.aethexai.com/recordings."""
        from aethexai._generated.api.recordings import (
            get_recording_api_v1_recordings_recording_id_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(recording_id)))

    def delete_recording(self, recording_id: str | UUID) -> Any:
        """Delete a recording. See https://docs.aethexai.com/recordings."""
        from aethexai._generated.api.recordings import (
            delete_recording_api_v1_recordings_recording_id_delete as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(recording_id)))

    def get_recording_audio(self, recording_id: str | UUID) -> Any:
        """Get recording audio download metadata. See https://docs.aethexai.com/recordings."""
        from aethexai._generated.api.recordings import (
            get_recording_audio_api_v1_recordings_recording_id_audio_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(recording_id)))

    # ─── transcription ─────────────────────────────────────────────────

    def transcribe_audio(self, *, body: Any) -> Any:
        """Synchronously transcribe an audio file (multipart). See https://docs.aethexai.com/transcription."""
        from aethexai._generated.api.transcription import (
            transcribe_sync_api_v1_transcribe_post as _op,
        )

        return self._call(_op.sync_detailed, body=body)

    def transcribe_audio_by_upload(self, **fields: Any) -> Any:
        """Synchronously transcribe a previously uploaded file. See https://docs.aethexai.com/transcription."""
        from aethexai._generated.api.transcription import (
            transcribe_sync_by_upload_api_v1_transcribe_by_upload_post as _op,
        )
        from aethexai._generated.models.transcribe_by_upload_request import (
            TranscribeByUploadRequest,
        )

        return self._call(_op.sync_detailed, body=build_body(TranscribeByUploadRequest, fields))

    def transcribe_audio_async(self, *, body: Any) -> Any:
        """Submit an async transcription job (multipart). See https://docs.aethexai.com/transcription."""
        from aethexai._generated.api.transcription import (
            transcribe_async_api_v1_transcribe_async_post as _op,
        )

        return self._call(_op.sync_detailed, body=body)

    def transcribe_audio_async_by_upload(self, **fields: Any) -> Any:
        """Submit an async transcription job for a previously uploaded file. See https://docs.aethexai.com/transcription."""
        from aethexai._generated.api.transcription import (
            transcribe_async_by_upload_api_v1_transcribe_async_by_upload_post as _op,
        )
        from aethexai._generated.models.transcribe_async_by_upload_request import (
            TranscribeAsyncByUploadRequest,
        )

        return self._call(
            _op.sync_detailed, body=build_body(TranscribeAsyncByUploadRequest, fields)
        )

    def get_transcription_job(self, job_id: str | UUID) -> Any:
        """Retrieve a transcription job by id. See https://docs.aethexai.com/transcription."""
        from aethexai._generated.api.transcription import (
            get_transcription_job_api_v1_transcribe_job_id_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(job_id)))

    def cancel_transcription_job(self, job_id: str | UUID) -> Any:
        """Cancel an in-flight transcription job. See https://docs.aethexai.com/transcription."""
        from aethexai._generated.api.transcription import (
            cancel_transcription_job_api_v1_transcribe_job_id_delete as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(job_id)))

    # ─── tts ───────────────────────────────────────────────────────────

    def synthesize_speech(self, **fields: Any) -> bytes:
        """Synthesize speech from text and return the raw audio bytes."""
        from aethexai._generated.models.tts_request import TTSRequest

        body = build_body(TTSRequest, fields)
        httpx_client = self._client.get_httpx_client()
        try:
            response = httpx_client.post(
                "/api/v1/tts",
                json=body.to_dict(),
                headers={"Content-Type": "application/json"},
            )
        except httpx.TimeoutException as exc:
            raise APITimeoutError() from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(cause=exc) from exc
        status = int(response.status_code)
        if 200 <= status < 300:
            return response.content
        raise _map_status_to_exception(status, response.content, response.headers)

    def stream_speech(self, *, chunk_size: int = 4096, **fields: Any) -> Iterator[bytes]:
        """Synthesize speech and yield audio chunks as they arrive."""
        from aethexai._generated.models.tts_stream_request import TTSStreamRequest

        body = build_body(TTSStreamRequest, fields)
        httpx_client = self._client.get_httpx_client()
        try:
            with httpx_client.stream(
                "POST",
                "/api/v1/tts/stream",
                json=body.to_dict(),
                headers={"Content-Type": "application/json"},
            ) as response:
                status = int(response.status_code)
                if not (200 <= status < 300):
                    response.read()
                    raise _map_status_to_exception(status, response.content, response.headers)
                yield from response.iter_bytes(chunk_size)
        except httpx.TimeoutException as exc:
            raise APITimeoutError() from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(cause=exc) from exc

    def batch_synthesize(self, **fields: Any) -> Any:
        """Submit a TTS batch job. See https://docs.aethexai.com/tts."""
        from aethexai._generated.api.tts import batch_synthesize_api_v1_tts_batch_post as _op
        from aethexai._generated.models.tts_batch_create import TTSBatchCreate

        return self._call(_op.sync_detailed, body=build_body(TTSBatchCreate, fields))

    def get_tts_batch(self, batch_id: str | UUID) -> Any:
        """Retrieve a TTS batch by id. See https://docs.aethexai.com/tts."""
        from aethexai._generated.api.tts import get_batch_api_v1_tts_batch_batch_id_get as _op

        return self._call(_op.sync_detailed, UUID(str(batch_id)))

    # ─── uploads ───────────────────────────────────────────────────────

    def presign_upload(self, **fields: Any) -> Any:
        """Request a presigned URL for direct file upload. See https://docs.aethexai.com/uploads."""
        from aethexai._generated.api.uploads import (
            presign_upload_api_v1_uploads_presign_post as _op,
        )
        from aethexai._generated.models.presign_upload_request import PresignUploadRequest

        return self._call(_op.sync_detailed, body=build_body(PresignUploadRequest, fields))

    # ─── usage ─────────────────────────────────────────────────────────

    def get_usage(self) -> Any:
        """Get usage details for the current period. See https://docs.aethexai.com/usage."""
        from aethexai._generated.api.usage import get_usage_api_v1_usage_get as _op

        return self._call(_op.sync_detailed)

    def get_usage_summary(self) -> Any:
        """Get a usage summary for the current period. See https://docs.aethexai.com/usage."""
        from aethexai._generated.api.usage import get_usage_summary_api_v1_usage_summary_get as _op

        return self._call(_op.sync_detailed)

    def get_daily_usage(self, *, days: int | Unset = 30) -> Any:
        """Get usage broken down by day. See https://docs.aethexai.com/usage."""
        from aethexai._generated.api.usage import get_daily_usage_api_v1_usage_daily_get as _op

        return self._call(_op.sync_detailed, days=days)

    def get_monthly_usage(self) -> Any:
        """Get usage broken down by month. See https://docs.aethexai.com/usage."""
        from aethexai._generated.api.usage import get_monthly_usage_api_v1_usage_monthly_get as _op

        return self._call(_op.sync_detailed)

    def list_triggers(self) -> Any:
        """List usage triggers (webhook subscriptions). See https://docs.aethexai.com/triggers."""
        from aethexai._generated.api.usage import list_triggers_api_v1_usage_triggers_get as _op

        return self._call(_op.sync_detailed)

    def create_trigger(self, **fields: Any) -> Any:
        """Create a usage trigger. See https://docs.aethexai.com/triggers."""
        from aethexai._generated.api.usage import create_trigger_api_v1_usage_triggers_post as _op
        from aethexai._generated.models.usage_trigger_create import UsageTriggerCreate

        return self._call(_op.sync_detailed, body=build_body(UsageTriggerCreate, fields))

    def update_trigger(self, trigger_id: str | UUID, **fields: Any) -> Any:
        """Update a usage trigger. See https://docs.aethexai.com/triggers."""
        from aethexai._generated.api.usage import (
            update_trigger_api_v1_usage_triggers_trigger_id_patch as _op,
        )
        from aethexai._generated.models.usage_trigger_update import UsageTriggerUpdate

        return self._call(
            _op.sync_detailed, UUID(str(trigger_id)), body=build_body(UsageTriggerUpdate, fields)
        )

    def list_trigger_firings(self, trigger_id: str | UUID, *, limit: int | Unset = 50) -> Any:
        """List recent firings for a trigger. See https://docs.aethexai.com/triggers."""
        from aethexai._generated.api.usage import (
            list_trigger_firings_api_v1_usage_triggers_trigger_id_firings_get as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(trigger_id)), limit=limit)

    def redeliver_firing(self, trigger_id: str | UUID, firing_id: str | UUID) -> Any:
        """Re-deliver a webhook firing. See https://docs.aethexai.com/triggers."""
        from aethexai._generated.api.usage import (
            redeliver_firing_api_v1_usage_triggers_trigger_id_firings_firing_id_redeliver_post as _op,
        )

        return self._call(_op.sync_detailed, UUID(str(trigger_id)), UUID(str(firing_id)))

    def rotate_webhook_secret(self) -> Any:
        """Rotate the tenant-level webhook signing secret. See https://docs.aethexai.com/triggers."""
        from aethexai._generated.api.usage import (
            rotate_webhook_secret_api_v1_usage_webhook_secret_rotate_post as _op,
        )

        return self._call(_op.sync_detailed)

    # ─── voices ────────────────────────────────────────────────────────

    def list_voices(
        self,
        *,
        language: str | None | Unset = UNSET,
        supports_dialect_style: bool | None | Unset = UNSET,
        tag: str | None | Unset = UNSET,
        limit: int | Unset = 100,
        offset: int | Unset = 0,
    ) -> Any:
        """List available voices. See https://docs.aethexai.com/voices."""
        from aethexai._generated.api.voices import list_voices_api_v1_voices_get as _op

        return self._call(
            _op.sync_detailed,
            language=language,
            supports_dialect_style=supports_dialect_style,
            tag=tag,
            limit=limit,
            offset=offset,
        )

    def get_voice(self, voice_id: str) -> Any:
        """Retrieve a voice by id. See https://docs.aethexai.com/voices."""
        from aethexai._generated.api.voices import get_voice_api_v1_voices_voice_id_get as _op

        return self._call(_op.sync_detailed, voice_id)

    def preview_voice(self, **fields: Any) -> Any:
        """Generate a short preview clip for a voice. See https://docs.aethexai.com/voices."""
        from aethexai._generated.api.voices import preview_voice_api_v1_voices_preview_post as _op
        from aethexai._generated.models.voice_preview_request import VoicePreviewRequest

        return self._call(_op.sync_detailed, body=build_body(VoicePreviewRequest, fields))
