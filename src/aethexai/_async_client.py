"""Asynchronous Aethex AI client with a flat-method API.

This module exposes ``AsyncAethexAI``, an asyncio-native counterpart to
``AethexAI`` with the same flat-method surface.

Example::

    from aethexai import AsyncAethexAI

    async with AsyncAethexAI(api_key="ak_live_...") as client:
        agent = await client.create_agent(name="Bot", system_prompt="You are helpful.")
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from typing import Any, cast
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
from aethexai._generated.models.agent_response import AgentResponse
from aethexai._generated.models.call_response import CallResponse
from aethexai._generated.models.conversation_response import ConversationResponse
from aethexai._generated.models.paginated_response import PaginatedResponse
from aethexai._generated.types import UNSET, Unset

_DEFAULT_BASE_URL = "https://api.aethexai.com"


class AsyncAethexAI:
    """Asynchronous Aethex AI client.

    Args:
        api_key: Aethex API key. Falls back to the ``AETHEX_API_KEY`` env var.
        base_url: API base URL. Defaults to https://api.aethexai.com.
        timeout: Per-request timeout in seconds.
        max_retries: Number of HTTP-level retries (wired via httpx transport).
        httpx_client: Optional pre-built ``httpx.AsyncClient`` to use as the transport.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 2,
        httpx_client: httpx.AsyncClient | None = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("AETHEX_API_KEY", "")
        if not resolved_key:
            raise AuthenticationError(
                "API key is required. Pass api_key= or set the AETHEX_API_KEY env var.",
                code="authentication_error",
                status_code=401,
            )
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

        httpx_args: dict[str, Any] = {
            "transport": httpx.AsyncHTTPTransport(retries=max_retries),
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
            self._client.set_async_httpx_client(httpx_client)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(base_url={self._base_url!r}, timeout={self._timeout!r})"

    async def close(self) -> None:
        """Close the underlying async HTTP client."""
        inner = self._client.get_async_httpx_client()
        await inner.aclose()

    async def __aenter__(self) -> AsyncAethexAI:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def _call(self, op_func: Any, *args: Any, **kwargs: Any) -> Any:
        """Run a generated ``asyncio_detailed`` op, raise on non-2xx, return parsed."""
        try:
            response = await op_func(*args, client=self._client, **kwargs)
        except httpx.TimeoutException as exc:
            raise APITimeoutError() from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(cause=exc) from exc
        status = int(response.status_code)
        if 200 <= status < 300:
            return response.parsed
        raise _map_status_to_exception(status, response.content, response.headers)

    async def list_agents(
        self, *, offset: int | Unset = 0, limit: int | Unset = 50
    ) -> PaginatedResponse[AgentResponse]:
        """List agents.

        Returns a single-page ``PaginatedResponse``; ``.data`` items are
        ``AgentResponse`` instances. Use ``.has_more`` to detect additional pages.
        """
        from aethexai._generated.api.agents import list_agents_api_v1_agents_get as _op

        return cast(
            PaginatedResponse[AgentResponse],
            await self._call(_op.asyncio_detailed, offset=offset, limit=limit),
        )

    async def create_agent(self, **fields: Any) -> Any:
        """Create a new agent."""
        from aethexai._generated.api.agents import create_agent_api_v1_agents_post as _op
        from aethexai._generated.models.agent_create import AgentCreate

        return await self._call(_op.asyncio_detailed, body=build_body(AgentCreate, fields))

    async def get_agent(self, agent_id: str | UUID) -> Any:
        """Retrieve an agent by id."""
        from aethexai._generated.api.agents import get_agent_api_v1_agents_agent_id_get as _op

        return await self._call(_op.asyncio_detailed, UUID(str(agent_id)))

    async def update_agent(self, agent_id: str | UUID, **fields: Any) -> Any:
        """Update an existing agent."""
        from aethexai._generated.api.agents import update_agent_api_v1_agents_agent_id_patch as _op
        from aethexai._generated.models.agent_update import AgentUpdate

        return await self._call(
            _op.asyncio_detailed, UUID(str(agent_id)), body=build_body(AgentUpdate, fields)
        )

    async def delete_agent(self, agent_id: str | UUID) -> Any:
        """Delete an agent."""
        from aethexai._generated.api.agents import delete_agent_api_v1_agents_agent_id_delete as _op

        return await self._call(_op.asyncio_detailed, UUID(str(agent_id)))

    async def duplicate_agent(self, agent_id: str | UUID) -> Any:
        """Duplicate an existing agent."""
        from aethexai._generated.api.agents import (
            duplicate_agent_api_v1_agents_agent_id_duplicate_post as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(agent_id)))

    async def list_agent_tools(self, agent_id: str | UUID) -> Any:
        """List tools for an agent."""
        from aethexai._generated.api.agents import (
            list_tools_api_v1_agents_agent_id_tools_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(agent_id)))

    async def add_agent_tool(self, agent_id: str | UUID, **fields: Any) -> Any:
        """Attach a tool to an agent."""
        from aethexai._generated.api.agents import add_tool_api_v1_agents_agent_id_tools_post as _op
        from aethexai._generated.models.agent_tool_create import AgentToolCreate

        return await self._call(
            _op.asyncio_detailed, UUID(str(agent_id)), body=build_body(AgentToolCreate, fields)
        )

    async def update_agent_tool(
        self, agent_id: str | UUID, tool_id: str | UUID, **fields: Any
    ) -> Any:
        """Update an agent tool."""
        from aethexai._generated.api.agents import (
            update_tool_api_v1_agents_agent_id_tools_tool_id_patch as _op,
        )
        from aethexai._generated.models.agent_tool_update import AgentToolUpdate

        return await self._call(
            _op.asyncio_detailed,
            UUID(str(agent_id)),
            UUID(str(tool_id)),
            body=build_body(AgentToolUpdate, fields),
        )

    async def delete_agent_tool(self, agent_id: str | UUID, tool_id: str | UUID) -> Any:
        """Detach a tool from an agent."""
        from aethexai._generated.api.agents import (
            delete_tool_api_v1_agents_agent_id_tools_tool_id_delete as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(agent_id)), UUID(str(tool_id)))

    async def list_knowledge_docs(self, agent_id: str | UUID) -> Any:
        """List knowledge-base documents for an agent."""
        from aethexai._generated.api.agents import (
            list_knowledge_docs_api_v1_agents_agent_id_knowledge_base_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(agent_id)))

    async def upload_knowledge_doc(self, agent_id: str | UUID, *, body: Any | Unset = UNSET) -> Any:
        """Upload a knowledge-base document (multipart)."""
        from aethexai._generated.api.agents import (
            upload_knowledge_doc_api_v1_agents_agent_id_knowledge_base_post as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(agent_id)), body=body)

    async def upload_knowledge_doc_by_upload(self, agent_id: str | UUID, **fields: Any) -> Any:
        """Attach a previously presigned upload as a knowledge-base doc."""
        from aethexai._generated.api.agents import (
            upload_knowledge_doc_by_upload_api_v1_agents_agent_id_knowledge_base_by_upload_post as _op,
        )
        from aethexai._generated.models.knowledge_doc_by_upload_request import (
            KnowledgeDocByUploadRequest,
        )

        return await self._call(
            _op.asyncio_detailed,
            UUID(str(agent_id)),
            body=build_body(KnowledgeDocByUploadRequest, fields),
        )

    async def delete_knowledge_doc(self, agent_id: str | UUID, doc_id: str | UUID) -> Any:
        """Delete a knowledge-base document."""
        from aethexai._generated.api.agents import (
            delete_knowledge_doc_api_v1_agents_agent_id_knowledge_base_doc_id_delete as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(agent_id)), UUID(str(doc_id)))

    async def process_knowledge_doc(self, agent_id: str | UUID, doc_id: str | UUID) -> Any:
        """Re-process a knowledge-base document."""
        from aethexai._generated.api.agents import (
            process_knowledge_doc_api_v1_agents_agent_id_knowledge_base_doc_id_process_post as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(agent_id)), UUID(str(doc_id)))

    async def get_knowledge_texts(self, agent_id: str | UUID) -> Any:
        """Fetch raw knowledge-base text snippets for an agent."""
        from aethexai._generated.api.agents import (
            get_knowledge_texts_api_v1_agents_agent_id_knowledge_base_texts_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(agent_id)))

    async def query_knowledge_base(self, agent_id: str | UUID, **fields: Any) -> Any:
        """Query an agent's knowledge base."""
        from aethexai._generated.api.agents import (
            query_knowledge_base_api_v1_agents_agent_id_knowledge_base_query_post as _op,
        )
        from aethexai._generated.models.knowledge_query_request import KnowledgeQueryRequest

        return await self._call(
            _op.asyncio_detailed,
            UUID(str(agent_id)),
            body=build_body(KnowledgeQueryRequest, fields),
        )

    async def list_api_keys(self) -> Any:
        """List API keys."""
        from aethexai._generated.api.api_keys import list_api_keys_api_v1_api_keys_get as _op

        return await self._call(_op.asyncio_detailed)

    async def create_api_key(self, **fields: Any) -> Any:
        """Create a new API key."""
        from aethexai._generated.api.api_keys import create_api_key_api_v1_api_keys_post as _op
        from aethexai._generated.models.api_key_create import APIKeyCreate

        return await self._call(_op.asyncio_detailed, body=build_body(APIKeyCreate, fields))

    async def revoke_api_key(self, key_id: str | UUID) -> Any:
        """Revoke an API key."""
        from aethexai._generated.api.api_keys import (
            revoke_api_key_api_v1_api_keys_key_id_delete as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(key_id)))

    async def rotate_api_key(self, key_id: str | UUID) -> Any:
        """Rotate an API key."""
        from aethexai._generated.api.api_keys import (
            rotate_api_key_api_v1_api_keys_key_id_rotate_post as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(key_id)))

    async def list_calls(
        self,
        *,
        status: str | None | Unset = UNSET,
        direction: Any | None | Unset = UNSET,
        offset: int | Unset = 0,
        limit: int | Unset = 50,
    ) -> PaginatedResponse[CallResponse]:
        """List calls.

        Returns a single-page ``PaginatedResponse``; ``.data`` items are
        ``CallResponse`` instances. Use ``.has_more`` to detect additional pages.
        """
        from aethexai._generated.api.calls import list_calls_api_v1_calls_get as _op

        return cast(
            PaginatedResponse[CallResponse],
            await self._call(
                _op.asyncio_detailed,
                status=status,
                direction=direction,
                offset=offset,
                limit=limit,
            ),
        )

    async def create_call_record(self, **fields: Any) -> Any:
        """Create a call record."""
        from aethexai._generated.api.calls import create_call_record_api_v1_calls_post as _op
        from aethexai._generated.models.call_record_create import CallRecordCreate

        return await self._call(_op.asyncio_detailed, body=build_body(CallRecordCreate, fields))

    async def get_call(self, call_id: str | UUID) -> Any:
        """Retrieve a call by id."""
        from aethexai._generated.api.calls import get_call_api_v1_calls_call_id_get as _op

        return await self._call(_op.asyncio_detailed, UUID(str(call_id)))

    async def get_call_status(self, call_id: str | UUID) -> Any:
        """Get a call's current status."""
        from aethexai._generated.api.calls import (
            get_call_status_api_v1_calls_call_id_status_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(call_id)))

    async def trigger_call(self, **fields: Any) -> Any:
        """Place an outbound call."""
        from aethexai._generated.api.calls import trigger_call_api_v1_calls_trigger_post as _op
        from aethexai._generated.models.call_create import CallCreate

        return await self._call(_op.asyncio_detailed, body=build_body(CallCreate, fields))

    async def batch_calls(self, **fields: Any) -> Any:
        """Trigger a batch of outbound calls."""
        from aethexai._generated.api.calls import batch_calls_api_v1_calls_batch_post as _op
        from aethexai._generated.models.batch_call_create import BatchCallCreate

        return await self._call(_op.asyncio_detailed, body=build_body(BatchCallCreate, fields))

    async def get_call_batch(self, batch_id: str | UUID) -> Any:
        """Retrieve a call batch by id."""
        from aethexai._generated.api.calls import get_batch_api_v1_calls_batch_batch_id_get as _op

        return await self._call(_op.asyncio_detailed, UUID(str(batch_id)))

    async def conversation_connect(self, **fields: Any) -> Any:
        """Establish a new conversation session."""
        from aethexai._generated.api.conversation import (
            connect_api_v1_conversation_connect_post as _op,
        )
        from aethexai._generated.models.connect_request import ConnectRequest

        return await self._call(_op.asyncio_detailed, body=build_body(ConnectRequest, fields))

    async def end_conversation_session(self, session_id: str) -> Any:
        """End a live conversation session."""
        from aethexai._generated.api.conversation import (
            end_session_api_v1_conversation_session_id_end_post as _op,
        )

        return await self._call(_op.asyncio_detailed, session_id)

    async def get_conversation_session_status(self, session_id: str) -> Any:
        """Get a conversation session's status."""
        from aethexai._generated.api.conversation import (
            get_session_status_api_v1_conversation_session_id_status_get as _op,
        )

        return await self._call(_op.asyncio_detailed, session_id)

    async def send_ice_candidate(self, session_id: str, **fields: Any) -> Any:
        """Send trickle-ICE candidates for a WebRTC session.

        Despite the singular method name, the request body takes a **list**
        of candidates plus the peer-connection id — there is no singular
        ``candidate`` field. Pass these keyword arguments:

        * ``candidates`` (``list[dict]``, required): one or more ICE candidate
          patches. Each dict needs ``candidate`` (the SDP candidate string),
          ``sdp_mid`` (``str``), and ``sdp_mline_index`` (``int``).
        * ``pc_id`` (``str``, required): the peer-connection id returned when
          the session was established.

        Example::

            await client.send_ice_candidate(
                session_id,
                pc_id="pc-123",
                candidates=[
                    {
                        "candidate": "candidate:1 1 udp 2122260223 10.0.0.1 54321 typ host",
                        "sdp_mid": "0",
                        "sdp_mline_index": 0,
                    }
                ],
            )

        Passing a singular ``candidate=`` keyword raises ``ValidationError``
        for the missing required ``candidates`` / ``pc_id`` fields.
        """
        from aethexai._generated.api.conversation import (
            ice_candidate_api_v1_conversation_session_id_ice_patch as _op,
        )
        from aethexai._generated.models.small_web_rtc_patch_request import SmallWebRTCPatchRequest

        return await self._call(
            _op.asyncio_detailed, session_id, body=build_body(SmallWebRTCPatchRequest, fields)
        )

    async def send_offer(self, session_id: str, **fields: Any) -> Any:
        """Send an SDP offer for a WebRTC session."""
        from aethexai._generated.api.conversation import (
            offer_api_v1_conversation_session_id_offer_post as _op,
        )
        from aethexai._generated.models.small_web_rtc_request import SmallWebRTCRequest

        return await self._call(
            _op.asyncio_detailed, session_id, body=build_body(SmallWebRTCRequest, fields)
        )

    async def send_tool_result(self, session_id: str, **fields: Any) -> Any:
        """Return a tool-call result to a live conversation."""
        from aethexai._generated.api.conversation import (
            tool_result_api_v1_conversation_session_id_tool_result_post as _op,
        )
        from aethexai._generated.models.tool_result_request import ToolResultRequest

        return await self._call(
            _op.asyncio_detailed, session_id, body=build_body(ToolResultRequest, fields)
        )

    async def list_conversations(
        self, *, offset: int | Unset = 0, limit: int | Unset = 50
    ) -> PaginatedResponse[ConversationResponse]:
        """List conversations.

        Returns a single-page ``PaginatedResponse``; ``.data`` items are
        ``ConversationResponse`` instances. Use ``.has_more`` to detect additional pages.
        """
        from aethexai._generated.api.conversations import (
            list_conversations_api_v1_conversations_get as _op,
        )

        return cast(
            PaginatedResponse[ConversationResponse],
            await self._call(_op.asyncio_detailed, offset=offset, limit=limit),
        )

    async def get_conversation(self, conversation_id: str | UUID) -> Any:
        """Retrieve a conversation by id."""
        from aethexai._generated.api.conversations import (
            get_conversation_api_v1_conversations_conversation_id_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(conversation_id)))

    async def get_transcript(self, conversation_id: str | UUID) -> Any:
        """Fetch a conversation transcript."""
        from aethexai._generated.api.conversations import (
            get_transcript_api_v1_conversations_conversation_id_transcript_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(conversation_id)))

    async def get_audio(self, conversation_id: str | UUID) -> Any:
        """Get audio metadata for a conversation."""
        from aethexai._generated.api.conversations import (
            get_audio_api_v1_conversations_conversation_id_audio_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(conversation_id)))

    async def stream_audio(
        self,
        conversation_id: str | UUID,
        *,
        token: str | None | Unset = UNSET,
        range_: str | None | Unset = UNSET,
    ) -> bytes:
        """Fetch raw conversation audio (WAV) and return the bytes.

        The 200 response is ``audio/wav`` even though ``openapi.json`` declares it
        as ``application/json``; we bypass the generated parser to avoid a
        ``UnicodeDecodeError``. Mirrors :meth:`synthesize_speech`.
        """
        from urllib.parse import quote

        params: dict[str, Any] = {}
        if not isinstance(token, Unset) and token is not None:
            params["token"] = token
        headers: dict[str, str] = {}
        if not isinstance(range_, Unset) and range_ is not None:
            headers["Range"] = range_

        url = "/api/v1/conversations/{conversation_id}/audio.wav".format(
            conversation_id=quote(str(UUID(str(conversation_id))), safe=""),
        )
        httpx_client = self._client.get_async_httpx_client()
        try:
            response = await httpx_client.get(url, params=params, headers=headers)
        except httpx.TimeoutException as exc:
            raise APITimeoutError() from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(cause=exc) from exc
        status = int(response.status_code)
        if 200 <= status < 300:
            return response.content
        raise _map_status_to_exception(status, response.content, response.headers)

    async def revoke_audio_token(self, conversation_id: str | UUID, **fields: Any) -> Any:
        """Revoke an audio playback token."""
        from aethexai._generated.api.conversations import (
            revoke_audio_token_api_v1_conversations_conversation_id_audio_revoke_post as _op,
        )
        from aethexai._generated.models.audio_revoke_body import AudioRevokeBody

        return await self._call(
            _op.asyncio_detailed,
            UUID(str(conversation_id)),
            body=build_body(AudioRevokeBody, fields),
        )

    async def submit_feedback(self, conversation_id: str | UUID, **fields: Any) -> Any:
        """Submit feedback on a conversation."""
        from aethexai._generated.api.conversations import (
            submit_feedback_api_v1_conversations_conversation_id_feedback_post as _op,
        )
        from aethexai._generated.models.conversation_feedback import ConversationFeedback

        return await self._call(
            _op.asyncio_detailed,
            UUID(str(conversation_id)),
            body=build_body(ConversationFeedback, fields),
        )

    async def search_conversations(self, q: str, *, limit: int | Unset = 20) -> Any:
        """Search conversations."""
        from aethexai._generated.api.conversations import (
            search_conversations_api_v1_conversations_search_get as _op,
        )

        return await self._call(_op.asyncio_detailed, q=q, limit=limit)

    async def list_models(self, *, include_unavailable: bool | Unset = False) -> Any:
        """List available LLM and voice models."""
        from aethexai._generated.api.models import list_models_api_v1_models_get as _op

        return await self._call(_op.asyncio_detailed, include_unavailable=include_unavailable)

    async def list_phone_numbers(self, *, offset: int | Unset = 0, limit: int | Unset = 50) -> Any:
        """List provisioned phone numbers."""
        from aethexai._generated.api.phone_numbers import (
            list_phone_numbers_api_v1_phone_numbers_get as _op,
        )

        return await self._call(_op.asyncio_detailed, offset=offset, limit=limit)

    async def get_phone_number(self, pn_id: str | UUID) -> Any:
        """Retrieve a phone number by id."""
        from aethexai._generated.api.phone_numbers import (
            get_phone_number_api_v1_phone_numbers_pn_id_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(pn_id)))

    async def update_phone_number(self, pn_id: str | UUID, **fields: Any) -> Any:
        """Update a phone number's configuration."""
        from aethexai._generated.api.phone_numbers import (
            update_phone_number_api_v1_phone_numbers_pn_id_patch as _op,
        )
        from aethexai._generated.models.phone_number_update import PhoneNumberUpdate

        return await self._call(
            _op.asyncio_detailed, UUID(str(pn_id)), body=build_body(PhoneNumberUpdate, fields)
        )

    async def release_phone_number(self, pn_id: str | UUID) -> Any:
        """Release (deprovision) a phone number."""
        from aethexai._generated.api.phone_numbers import (
            release_phone_number_api_v1_phone_numbers_pn_id_delete as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(pn_id)))

    async def set_phone_number_routing(self, pn_id: str | UUID, **fields: Any) -> Any:
        """Configure inbound routing for a phone number."""
        from aethexai._generated.api.phone_numbers import (
            set_routing_api_v1_phone_numbers_pn_id_routing_post as _op,
        )
        from aethexai._generated.models.inbound_routing_config import InboundRoutingConfig

        return await self._call(
            _op.asyncio_detailed,
            UUID(str(pn_id)),
            body=build_body(InboundRoutingConfig, fields),
        )

    async def register_sip_phone_number(self, **fields: Any) -> Any:
        """Register an externally-hosted SIP phone number."""
        from aethexai._generated.api.phone_numbers import (
            register_sip_api_v1_phone_numbers_sip_register_post as _op,
        )
        from aethexai._generated.models.sip_register_request import SipRegisterRequest

        return await self._call(_op.asyncio_detailed, body=build_body(SipRegisterRequest, fields))

    async def register_twilio_phone_number(self, **fields: Any) -> Any:
        """Register a Twilio-managed phone number."""
        from aethexai._generated.api.phone_numbers import (
            register_twilio_api_v1_phone_numbers_twilio_register_post as _op,
        )
        from aethexai._generated.models.twilio_register_request import TwilioRegisterRequest

        return await self._call(
            _op.asyncio_detailed, body=build_body(TwilioRegisterRequest, fields)
        )

    async def register_twilio_account(self, **fields: Any) -> Any:
        """Register a Bring-Your-Own Twilio account."""
        from aethexai._generated.api.twilio_accounts import (
            register_twilio_account_api_v1_twilio_accounts_post as _op,
        )
        from aethexai._generated.models.twilio_account_create import TwilioAccountCreate

        return await self._call(_op.asyncio_detailed, body=build_body(TwilioAccountCreate, fields))

    async def list_twilio_accounts(
        self, *, offset: int | Unset = 0, limit: int | Unset = 50
    ) -> Any:
        """List Twilio accounts available to the tenant."""
        from aethexai._generated.api.twilio_accounts import (
            list_twilio_accounts_api_v1_twilio_accounts_get as _op,
        )

        return await self._call(_op.asyncio_detailed, offset=offset, limit=limit)

    async def get_twilio_account(self, account_id: str | UUID) -> Any:
        """Retrieve a Twilio account by id."""
        from aethexai._generated.api.twilio_accounts import (
            get_twilio_account_api_v1_twilio_accounts_account_id_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(account_id)))

    async def release_twilio_account(self, account_id: str | UUID) -> Any:
        """Release a tenant-owned Twilio account."""
        from aethexai._generated.api.twilio_accounts import (
            release_twilio_account_api_v1_twilio_accounts_account_id_delete as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(account_id)))

    async def list_recordings(self, *, offset: int | Unset = 0, limit: int | Unset = 50) -> Any:
        """List recordings."""
        from aethexai._generated.api.recordings import list_recordings_api_v1_recordings_get as _op

        return await self._call(_op.asyncio_detailed, offset=offset, limit=limit)

    async def get_recording(self, recording_id: str | UUID) -> Any:
        """Retrieve a recording by id."""
        from aethexai._generated.api.recordings import (
            get_recording_api_v1_recordings_recording_id_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(recording_id)))

    async def delete_recording(self, recording_id: str | UUID) -> Any:
        """Delete a recording."""
        from aethexai._generated.api.recordings import (
            delete_recording_api_v1_recordings_recording_id_delete as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(recording_id)))

    async def get_recording_audio(self, recording_id: str | UUID) -> Any:
        """Get recording audio download metadata."""
        from aethexai._generated.api.recordings import (
            get_recording_audio_api_v1_recordings_recording_id_audio_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(recording_id)))

    async def transcribe_audio(self, *, body: Any) -> Any:
        """Synchronously transcribe an audio file (multipart)."""
        from aethexai._generated.api.transcription import (
            transcribe_sync_api_v1_transcribe_post as _op,
        )
        from aethexai._transcription import (
            build_sync_body,
            coerce_to_bytes,
            merge_transcriptions,
            prepare_chunks,
        )

        data = coerce_to_bytes(getattr(body, "file", None))
        if data is None:
            return await self._call(_op.asyncio_detailed, body=body)
        chunks = prepare_chunks(data)
        if chunks is None:
            single = build_sync_body(
                data,
                file_name=body.file.file_name,
                mime_type=body.file.mime_type,
                language=body.language,
            )
            return await self._call(_op.asyncio_detailed, body=single)
        if len(chunks) == 1:
            return await self._call(
                _op.asyncio_detailed,
                body=build_sync_body(
                    chunks[0], file_name="audio.wav", mime_type="audio/wav", language=body.language
                ),
            )
        return merge_transcriptions(
            [
                await self._call(
                    _op.asyncio_detailed,
                    body=build_sync_body(
                        chunk, file_name="audio.wav", mime_type="audio/wav", language=body.language
                    ),
                )
                for chunk in chunks
            ]
        )

    async def transcribe_audio_by_upload(self, **fields: Any) -> Any:
        """Synchronously transcribe a previously uploaded file."""
        from aethexai._generated.api.transcription import (
            transcribe_sync_by_upload_api_v1_transcribe_by_upload_post as _op,
        )
        from aethexai._generated.models.transcribe_by_upload_request import (
            TranscribeByUploadRequest,
        )

        return await self._call(
            _op.asyncio_detailed, body=build_body(TranscribeByUploadRequest, fields)
        )

    async def transcribe_audio_async(self, *, body: Any) -> Any:
        """Submit an async transcription job (multipart)."""
        from aethexai._generated.api.transcription import (
            transcribe_async_api_v1_transcribe_async_post as _op,
        )
        from aethexai._transcription import guard_async_body

        return await self._call(_op.asyncio_detailed, body=guard_async_body(body))

    async def transcribe_audio_async_by_upload(self, **fields: Any) -> Any:
        """Submit an async transcription job for a previously uploaded file."""
        from aethexai._generated.api.transcription import (
            transcribe_async_by_upload_api_v1_transcribe_async_by_upload_post as _op,
        )
        from aethexai._generated.models.transcribe_async_by_upload_request import (
            TranscribeAsyncByUploadRequest,
        )

        return await self._call(
            _op.asyncio_detailed, body=build_body(TranscribeAsyncByUploadRequest, fields)
        )

    async def get_transcription_job(self, job_id: str | UUID) -> Any:
        """Retrieve a transcription job by id."""
        from aethexai._generated.api.transcription import (
            get_transcription_job_api_v1_transcribe_job_id_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(job_id)))

    async def cancel_transcription_job(self, job_id: str | UUID) -> Any:
        """Cancel an in-flight transcription job."""
        from aethexai._generated.api.transcription import (
            cancel_transcription_job_api_v1_transcribe_job_id_delete as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(job_id)))

    async def synthesize_speech(self, **fields: Any) -> bytes:
        """Synthesize speech from text and return the raw audio bytes."""
        from aethexai._generated.models.tts_request import TTSRequest

        body = build_body(TTSRequest, fields)
        httpx_client = self._client.get_async_httpx_client()
        try:
            response = await httpx_client.post(
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

    async def stream_speech(self, *, chunk_size: int = 4096, **fields: Any) -> AsyncIterator[bytes]:
        """Synthesize speech and yield audio chunks as they arrive."""
        from aethexai._generated.models.tts_stream_request import TTSStreamRequest

        body = build_body(TTSStreamRequest, fields)
        httpx_client = self._client.get_async_httpx_client()
        try:
            async with httpx_client.stream(
                "POST",
                "/api/v1/tts/stream",
                json=body.to_dict(),
                headers={"Content-Type": "application/json"},
            ) as response:
                status = int(response.status_code)
                if not (200 <= status < 300):
                    await response.aread()
                    raise _map_status_to_exception(status, response.content, response.headers)
                async for chunk in response.aiter_bytes(chunk_size):
                    yield chunk
        except httpx.TimeoutException as exc:
            raise APITimeoutError() from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(cause=exc) from exc

    async def batch_synthesize(self, **fields: Any) -> Any:
        """Submit a TTS batch job."""
        from aethexai._generated.api.tts import batch_synthesize_api_v1_tts_batch_post as _op
        from aethexai._generated.models.tts_batch_create import TTSBatchCreate

        return await self._call(_op.asyncio_detailed, body=build_body(TTSBatchCreate, fields))

    async def get_tts_batch(self, batch_id: str | UUID) -> Any:
        """Retrieve a TTS batch by id."""
        from aethexai._generated.api.tts import get_batch_api_v1_tts_batch_batch_id_get as _op

        return await self._call(_op.asyncio_detailed, UUID(str(batch_id)))

    async def presign_upload(self, **fields: Any) -> Any:
        """Request a presigned URL for direct file upload."""
        from aethexai._generated.api.uploads import (
            presign_upload_api_v1_uploads_presign_post as _op,
        )
        from aethexai._generated.models.presign_upload_request import PresignUploadRequest

        return await self._call(_op.asyncio_detailed, body=build_body(PresignUploadRequest, fields))

    async def get_usage(self) -> Any:
        """Get usage details for the current period."""
        from aethexai._generated.api.usage import get_usage_api_v1_usage_get as _op

        return await self._call(_op.asyncio_detailed)

    async def get_usage_summary(self) -> Any:
        """Get a usage summary for the current period."""
        from aethexai._generated.api.usage import get_usage_summary_api_v1_usage_summary_get as _op

        return await self._call(_op.asyncio_detailed)

    async def get_daily_usage(self, *, days: int | Unset = 30) -> Any:
        """Get usage broken down by day."""
        from aethexai._generated.api.usage import get_daily_usage_api_v1_usage_daily_get as _op

        return await self._call(_op.asyncio_detailed, days=days)

    async def get_monthly_usage(self) -> Any:
        """Get usage broken down by month."""
        from aethexai._generated.api.usage import get_monthly_usage_api_v1_usage_monthly_get as _op

        return await self._call(_op.asyncio_detailed)

    async def list_triggers(self) -> Any:
        """List usage triggers (webhook subscriptions)."""
        from aethexai._generated.api.usage import list_triggers_api_v1_usage_triggers_get as _op

        return await self._call(_op.asyncio_detailed)

    async def create_trigger(self, **fields: Any) -> Any:
        """Create a usage trigger."""
        from aethexai._generated.api.usage import create_trigger_api_v1_usage_triggers_post as _op
        from aethexai._generated.models.usage_trigger_create import UsageTriggerCreate

        return await self._call(_op.asyncio_detailed, body=build_body(UsageTriggerCreate, fields))

    async def update_trigger(self, trigger_id: str | UUID, **fields: Any) -> Any:
        """Update a usage trigger."""
        from aethexai._generated.api.usage import (
            update_trigger_api_v1_usage_triggers_trigger_id_patch as _op,
        )
        from aethexai._generated.models.usage_trigger_update import UsageTriggerUpdate

        return await self._call(
            _op.asyncio_detailed, UUID(str(trigger_id)), body=build_body(UsageTriggerUpdate, fields)
        )

    async def list_trigger_firings(self, trigger_id: str | UUID, *, limit: int | Unset = 50) -> Any:
        """List recent firings for a trigger."""
        from aethexai._generated.api.usage import (
            list_trigger_firings_api_v1_usage_triggers_trigger_id_firings_get as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(trigger_id)), limit=limit)

    async def redeliver_firing(self, trigger_id: str | UUID, firing_id: str | UUID) -> Any:
        """Re-deliver a webhook firing."""
        from aethexai._generated.api.usage import (
            redeliver_firing_api_v1_usage_triggers_trigger_id_firings_firing_id_redeliver_post as _op,
        )

        return await self._call(_op.asyncio_detailed, UUID(str(trigger_id)), UUID(str(firing_id)))

    async def rotate_webhook_secret(self) -> Any:
        """Rotate the tenant-level webhook signing secret."""
        from aethexai._generated.api.usage import (
            rotate_webhook_secret_api_v1_usage_webhook_secret_rotate_post as _op,
        )

        return await self._call(_op.asyncio_detailed)

    async def list_voices(
        self,
        *,
        language: str | None | Unset = UNSET,
        supports_dialect_style: bool | None | Unset = UNSET,
        tag: str | None | Unset = UNSET,
        limit: int | Unset = 100,
        offset: int | Unset = 0,
    ) -> Any:
        """List available voices."""
        from aethexai._generated.api.voices import list_voices_api_v1_voices_get as _op

        return await self._call(
            _op.asyncio_detailed,
            language=language,
            supports_dialect_style=supports_dialect_style,
            tag=tag,
            limit=limit,
            offset=offset,
        )

    async def get_voice(self, voice_id: str) -> Any:
        """Retrieve a voice by id."""
        from aethexai._generated.api.voices import get_voice_api_v1_voices_voice_id_get as _op

        return await self._call(_op.asyncio_detailed, voice_id)

    async def preview_voice(self, **fields: Any) -> bytes:
        """Generate a short preview clip for a voice and return audio bytes.

        The 200 response is ``audio/wav`` even though ``openapi.json`` declares it
        as ``application/json``; we bypass the generated parser to avoid a
        ``UnicodeDecodeError``. Mirrors :meth:`synthesize_speech`.
        """
        from aethexai._generated.models.voice_preview_request import VoicePreviewRequest

        body = build_body(VoicePreviewRequest, fields)
        httpx_client = self._client.get_async_httpx_client()
        try:
            response = await httpx_client.post(
                "/api/v1/voices/preview",
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

    async def list_tag_vocabulary(self) -> Any:
        """Return the closed tag vocabulary for voices."""
        from aethexai._generated.api.voices import (
            list_tag_vocabulary_api_v1_voices_tag_vocabulary_get as _op,
        )

        return await self._call(_op.asyncio_detailed)
