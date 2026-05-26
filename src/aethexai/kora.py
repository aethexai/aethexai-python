"""Kora — focused voice-only client for Aethex AI.

Kora is a flat, ergonomic wrapper around the generated REST client that
exposes only the voice-building surface of the Aethex API: agents, outbound
calls, voices, text-to-speech (kora_speak), transcription (kora_read), and
read-only conversation history.

Account-management endpoints (api keys, billing, dashboard, sip trunks,
phone numbers, webhooks, usage) intentionally live on :class:`AethexAI`,
not on Kora. Kora is for building voice agents, not running the account.

Example::

    from aethexai import Kora

    client = Kora("https://api.aethexai.com", "ae_live_...")
    agent = client.create_agent(
        name="Aethex Agent",
        system_prompt="You are a banking assistant.",
        first_message="Bonjour!",
        voice_id="fatima",
        language="french",
        dialect_style="local",
    )
    client.trigger_call(agent.id, to_number="+221...")
"""

from __future__ import annotations

from collections.abc import Iterator
from io import BytesIO
from typing import Any, BinaryIO
from uuid import UUID

import httpx

from aethexai._exceptions import (
    APIConnectionError,
    APITimeoutError,
    _map_status_to_exception,
)
from aethexai._generated.api.agents import (
    create_agent_api_v1_agents_post as _create_agent_op,
)
from aethexai._generated.api.agents import (
    delete_agent_api_v1_agents_agent_id_delete as _delete_agent_op,
)
from aethexai._generated.api.agents import (
    duplicate_agent_api_v1_agents_agent_id_duplicate_post as _duplicate_agent_op,
)
from aethexai._generated.api.agents import (
    get_agent_api_v1_agents_agent_id_get as _get_agent_op,
)
from aethexai._generated.api.agents import (
    list_agents_api_v1_agents_get as _list_agents_op,
)
from aethexai._generated.api.agents import (
    update_agent_api_v1_agents_agent_id_patch as _update_agent_op,
)
from aethexai._generated.api.calls import (
    get_call_api_v1_calls_call_id_get as _get_call_op,
)
from aethexai._generated.api.calls import (
    get_call_status_api_v1_calls_call_id_status_get as _get_call_status_op,
)
from aethexai._generated.api.calls import (
    list_calls_api_v1_calls_get as _list_calls_op,
)
from aethexai._generated.api.calls import (
    trigger_call_api_v1_calls_trigger_post as _trigger_call_op,
)
from aethexai._generated.api.conversations import (
    get_audio_api_v1_conversations_conversation_id_audio_get as _get_audio_url_op,
)
from aethexai._generated.api.conversations import (
    get_conversation_api_v1_conversations_conversation_id_get as _get_conversation_op,
)
from aethexai._generated.api.conversations import (
    get_transcript_api_v1_conversations_conversation_id_transcript_get as _get_transcript_op,
)
from aethexai._generated.api.conversations import (
    list_conversations_api_v1_conversations_get as _list_conversations_op,
)
from aethexai._generated.api.transcription import (
    get_transcription_job_api_v1_transcribe_job_id_get as _get_transcribe_job_op,
)
from aethexai._generated.api.transcription import (
    transcribe_async_api_v1_transcribe_async_post as _transcribe_async_op,
)
from aethexai._generated.api.transcription import (
    transcribe_sync_api_v1_transcribe_post as _transcribe_sync_op,
)
from aethexai._generated.api.tts import (
    synthesize_api_v1_tts_post as _synthesize_op,
)
from aethexai._generated.api.voices import (
    get_voice_api_v1_voices_voice_id_get as _get_voice_op,
)
from aethexai._generated.api.voices import (
    list_voices_api_v1_voices_get as _list_voices_op,
)
from aethexai._generated.client import AuthenticatedClient
from aethexai._generated.models.agent_create import AgentCreate
from aethexai._generated.models.agent_update import AgentUpdate
from aethexai._generated.models.body_transcribe_async_api_v1_transcribe_async_post import (
    BodyTranscribeAsyncApiV1TranscribeAsyncPost,
)
from aethexai._generated.models.body_transcribe_sync_api_v1_transcribe_post import (
    BodyTranscribeSyncApiV1TranscribePost,
)
from aethexai._generated.models.call_create import CallCreate
from aethexai._generated.models.tts_request import TTSRequest
from aethexai._generated.models.tts_stream_request import TTSStreamRequest
from aethexai._generated.models.voice_preview_request import VoicePreviewRequest
from aethexai._generated.types import UNSET, File

_DEFAULT_BASE_URL = "https://api.aethexai.com"


def _to_uuid(value: str | UUID) -> UUID:
    """Coerce a stringified UUID into a ``UUID`` instance for path templating."""
    return value if isinstance(value, UUID) else UUID(str(value))


def _as_file(
    file: bytes | BinaryIO | File,
    *,
    file_name: str | None = None,
    mime_type: str | None = None,
) -> File:
    """Normalize raw bytes / streams / ``File`` objects into the generated ``File`` type."""
    if isinstance(file, File):
        return file
    if isinstance(file, (bytes, bytearray)):
        return File(
            payload=BytesIO(bytes(file)),
            file_name=file_name or "audio.bin",
            mime_type=mime_type or "application/octet-stream",
        )
    return File(payload=file, file_name=file_name, mime_type=mime_type)


class Kora:
    """Voice-only Aethex client with a flat method API.

    The constructor takes a positional ``base_url`` and ``api_key`` for the
    quickest possible start. Use :class:`aethexai.AethexAI` instead if you
    need account-management endpoints (api keys, billing, sip trunks, etc.).
    """

    def __init__(
        self,
        base_url: str = _DEFAULT_BASE_URL,
        api_key: str = "",
        *,
        timeout: float | None = None,
        verify_ssl: bool = True,
        raise_on_unexpected_status: bool = False,
    ) -> None:
        """Create a Kora client.

        Args:
            base_url: Aethex API base URL, e.g. ``https://api.aethexai.com``.
            api_key: API key sent as the ``X-API-Key`` header.
            timeout: Optional request timeout in seconds.
            verify_ssl: Whether to verify the API server's TLS certificate.
            raise_on_unexpected_status: Raise ``UnexpectedStatus`` for
                undocumented status codes instead of returning ``None``.
        """
        if not api_key:
            raise ValueError("api_key is required. Pass it positionally: Kora(base_url, api_key).")
        self._base_url = base_url
        # NOTE: api_key is intentionally NOT stored as an instance attribute.
        # See ``AethexAI.__init__`` for the rationale (finding A.5 of the
        # 2026-05-17 pre-launch audit). Kora was the easiest leak vector
        # because both ``Kora._api_key`` and ``AuthenticatedClient.token``
        # carried the same secret.
        timeout_arg: httpx.Timeout | None = httpx.Timeout(timeout) if timeout is not None else None
        self._client = AuthenticatedClient(
            base_url=base_url,
            token=api_key,
            auth_header_name="X-API-Key",
            prefix="",
            timeout=timeout_arg,
            verify_ssl=verify_ssl,
            raise_on_unexpected_status=raise_on_unexpected_status,
        )

    # ── Lifecycle ─────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        # See ``AethexAI.__repr__``.
        return f"{type(self).__name__}(base_url={self._base_url!r})"

    def close(self) -> None:
        """Close the underlying HTTP client."""
        client = self._client.get_httpx_client()
        client.close()

    def __enter__(self) -> Kora:
        """Enter a context manager that closes the HTTP client on exit."""
        self._client.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit the context manager and close the HTTP client."""
        self._client.__exit__(*args)

    # ── Internal request runner ───────────────────────────────────────────

    def _call(self, op_func: Any, *args: Any, **kwargs: Any) -> Any:
        """Run a generated ``sync_detailed`` op, raise on non-2xx, return parsed."""
        response = op_func(*args, client=self._client, **kwargs)
        status = int(response.status_code)
        if 200 <= status < 300:
            return response.parsed
        raise _map_status_to_exception(status, response.content, response.headers)

    def _call_bytes(self, op_func: Any, *args: Any, **kwargs: Any) -> bytes:
        """Variant of :meth:`_call` that returns the raw response body on 2xx."""
        response = op_func(*args, client=self._client, **kwargs)
        status = int(response.status_code)
        if 200 <= status < 300:
            content: bytes = response.content
            return content
        raise _map_status_to_exception(status, response.content, response.headers)

    # ── Agents ────────────────────────────────────────────────────────────

    def create_agent(
        self,
        name: str,
        system_prompt: str,
        voice_id: str,
        *,
        first_message: str | None = None,
        language: str | None = None,
        dialect_style: str | None = None,
        llm_model: str | None = None,
        stt_model: str | None = None,
        tts_model: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """Create a new voice agent."""
        body_kwargs: dict[str, Any] = {
            "name": name,
            "system_prompt": system_prompt,
            "voice_id": voice_id,
        }
        if first_message is not None:
            body_kwargs["first_message"] = first_message
        if language is not None:
            body_kwargs["language"] = language
        if dialect_style is not None:
            body_kwargs["dialect_style"] = dialect_style
        if llm_model is not None:
            body_kwargs["llm_model"] = llm_model
        if stt_model is not None:
            body_kwargs["stt_model"] = stt_model
        if tts_model is not None:
            body_kwargs["tts_model"] = tts_model
        body_kwargs.update(kwargs)
        return self._call(_create_agent_op.sync_detailed, body=AgentCreate(**body_kwargs))

    def get_agent(self, agent_id: str | UUID) -> Any:
        """Fetch a single agent by id."""
        return self._call(_get_agent_op.sync_detailed, _to_uuid(agent_id))

    def list_agents(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """List agents on the current account."""
        return self._call(
            _list_agents_op.sync_detailed,
            limit=limit if limit is not None else UNSET,
            offset=offset if offset is not None else UNSET,
        )

    def update_agent(self, agent_id: str | UUID, **kwargs: Any) -> Any:
        """Partially update an agent's configuration."""
        return self._call(
            _update_agent_op.sync_detailed,
            _to_uuid(agent_id),
            body=AgentUpdate(**kwargs),
        )

    def delete_agent(self, agent_id: str | UUID) -> Any:
        """Permanently delete an agent."""
        return self._call(_delete_agent_op.sync_detailed, _to_uuid(agent_id))

    def duplicate_agent(self, agent_id: str | UUID) -> Any:
        """Clone an agent, returning the new duplicate."""
        return self._call(_duplicate_agent_op.sync_detailed, _to_uuid(agent_id))

    # ── Calls (outbound voice) ────────────────────────────────────────────

    def trigger_call(
        self,
        agent_id: str | UUID,
        to_number: str,
        *,
        from_number: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """Trigger an outbound voice call from ``agent_id`` to ``to_number``."""
        body_kwargs: dict[str, Any] = {
            "agent_id": str(agent_id),
            "to_number": to_number,
        }
        if from_number is not None:
            body_kwargs["from_number"] = from_number
        body_kwargs.update(kwargs)
        return self._call(_trigger_call_op.sync_detailed, body=CallCreate(**body_kwargs))

    def get_call(self, call_id: str | UUID) -> Any:
        """Fetch a call record by id."""
        return self._call(_get_call_op.sync_detailed, _to_uuid(call_id))

    def list_calls(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """List recent calls on the current account."""
        return self._call(
            _list_calls_op.sync_detailed,
            limit=limit if limit is not None else UNSET,
            offset=offset if offset is not None else UNSET,
        )

    def get_call_status(self, call_id: str | UUID) -> Any:
        """Fetch the current status of a call."""
        return self._call(_get_call_status_op.sync_detailed, _to_uuid(call_id))

    # ── Voices ────────────────────────────────────────────────────────────

    def list_voices(
        self,
        *,
        language: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """List available TTS voices, optionally filtered by ``language``."""
        return self._call(
            _list_voices_op.sync_detailed,
            language=language if language is not None else UNSET,
            limit=limit if limit is not None else UNSET,
            offset=offset if offset is not None else UNSET,
        )

    def get_voice(self, voice_id: str) -> Any:
        """Fetch metadata for a single voice."""
        return self._call(_get_voice_op.sync_detailed, voice_id)

    def preview_voice(self, voice_id: str, text: str | None = None) -> bytes:
        """Generate a short voice preview for ``voice_id`` speaking ``text``.

        The 200 response is ``audio/wav`` even though ``openapi.json`` declares it
        as ``application/json``; we bypass the generated parser to avoid a
        ``UnicodeDecodeError`` (AET-1522). Mirrors :meth:`synthesize_speech`.
        """
        body_kwargs: dict[str, Any] = {"voice_id": voice_id}
        if text is not None:
            body_kwargs["text"] = text
        body = VoicePreviewRequest(**body_kwargs)
        httpx_client = self._client.get_httpx_client()
        try:
            response = httpx_client.post(
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

    # ── Text-to-speech (kora_speak) ───────────────────────────────────────

    def synthesize_speech(
        self,
        text: str,
        voice_id: str,
        *,
        language: str | None = None,
        **kwargs: Any,
    ) -> bytes:
        """Synthesize ``text`` to audio bytes using ``voice_id``.

        Returns the raw audio payload on success; raises a typed
        :class:`~aethexai.APIStatusError` subclass on any non-2xx response.
        """
        body_kwargs: dict[str, Any] = {"text": text, "voice_id": voice_id}
        if language is not None:
            body_kwargs["language"] = language
        body_kwargs.update(kwargs)
        return self._call_bytes(
            _synthesize_op.sync_detailed,
            body=TTSRequest(**body_kwargs),
        )

    def stream_speech(
        self,
        text: str,
        voice_id: str,
        *,
        language: str | None = None,
        chunk_size: int = 4096,
        **kwargs: Any,
    ) -> Iterator[bytes]:
        """Stream synthesized speech as an iterator of audio byte chunks.

        Returns chunked PCM16 audio at 24kHz. The first chunk arrives with
        lower latency than :meth:`synthesize_speech` because audio starts
        flowing as it is generated. Raises a typed
        :class:`~aethexai.APIStatusError` subclass if the initial response
        status indicates an error before chunks begin to flow.
        """
        body_kwargs: dict[str, Any] = {"text": text, "voice_id": voice_id}
        if language is not None:
            body_kwargs["language"] = language
        body_kwargs.update(kwargs)
        body = TTSStreamRequest(**body_kwargs)
        httpx_client = self._client.get_httpx_client()
        with httpx_client.stream(
            "POST",
            "/api/v1/tts/stream",
            json=body.to_dict(),
            headers={"Content-Type": "application/json"},
        ) as response:
            status = int(response.status_code)
            if not (200 <= status < 300):
                # Materialize the (small) error body so we can build a typed
                # exception consistent with every other Kora method.
                response.read()
                raise _map_status_to_exception(status, response.content, response.headers)
            yield from response.iter_bytes(chunk_size)

    # ── Transcription (kora_read) ─────────────────────────────────────────

    def transcribe(
        self,
        file: bytes | BinaryIO | File,
        *,
        language: str | None = None,
        file_name: str | None = None,
        mime_type: str | None = None,
    ) -> Any:
        """Transcribe an audio file synchronously, returning the full transcript."""
        body = BodyTranscribeSyncApiV1TranscribePost(
            file=_as_file(file, file_name=file_name, mime_type=mime_type),
            language=language if language is not None else UNSET,
        )
        return self._call(_transcribe_sync_op.sync_detailed, body=body)

    def transcribe_async(
        self,
        file: bytes | BinaryIO | File,
        *,
        language: str | None = None,
        webhook_url: str | None = None,
        file_name: str | None = None,
        mime_type: str | None = None,
    ) -> Any:
        """Submit an audio file for async transcription, returning a job handle."""
        body = BodyTranscribeAsyncApiV1TranscribeAsyncPost(
            file=_as_file(file, file_name=file_name, mime_type=mime_type),
            language=language if language is not None else UNSET,
            webhook_url=webhook_url if webhook_url is not None else UNSET,
        )
        return self._call(_transcribe_async_op.sync_detailed, body=body)

    def get_transcribe_job(self, job_id: str | UUID) -> Any:
        """Poll an async transcription job by id."""
        return self._call(_get_transcribe_job_op.sync_detailed, _to_uuid(job_id))

    # ── Conversations (read-only) ─────────────────────────────────────────

    def get_conversation(self, conversation_id: str | UUID) -> Any:
        """Fetch a single conversation record by id."""
        return self._call(_get_conversation_op.sync_detailed, _to_uuid(conversation_id))

    def list_conversations(
        self,
        *,
        agent_id: str | UUID | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """List conversations on the current account.

        Note: the underlying ``GET /api/v1/conversations`` endpoint does not
        support an ``agent_id`` filter; if one is supplied here it is applied
        client-side to the returned page.
        """
        result = self._call(
            _list_conversations_op.sync_detailed,
            limit=limit if limit is not None else UNSET,
            offset=offset if offset is not None else UNSET,
        )
        if agent_id is None or result is None:
            return result
        wanted = str(agent_id)
        data = getattr(result, "data", None)
        if isinstance(data, list):
            result.data = [
                item
                for item in data
                if str(
                    getattr(
                        item, "agent_id", item.get("agent_id") if isinstance(item, dict) else None
                    )
                )
                == wanted
            ]
        return result

    def get_conversation_transcript(self, conversation_id: str | UUID) -> Any:
        """Fetch the per-turn transcript for a conversation."""
        return self._call(_get_transcript_op.sync_detailed, _to_uuid(conversation_id))

    def get_conversation_audio(self, conversation_id: str | UUID) -> bytes:
        """Fetch the raw audio bytes for a conversation recording (WAV).

        The 200 response is ``audio/wav`` even though ``openapi.json`` declares it
        as ``application/json``; we bypass the generated parser to avoid a
        ``UnicodeDecodeError`` (AET-1522). Mirrors :meth:`synthesize_speech`.
        """
        from urllib.parse import quote

        url = "/api/v1/conversations/{conversation_id}/audio.wav".format(
            conversation_id=quote(str(_to_uuid(conversation_id)), safe=""),
        )
        httpx_client = self._client.get_httpx_client()
        try:
            response = httpx_client.get(url)
        except httpx.TimeoutException as exc:
            raise APITimeoutError() from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(cause=exc) from exc
        status = int(response.status_code)
        if 200 <= status < 300:
            return response.content
        raise _map_status_to_exception(status, response.content, response.headers)

    def get_conversation_audio_url(self, conversation_id: str | UUID) -> Any:
        """Fetch a short-lived signed URL pointing to the conversation audio."""
        return self._call(_get_audio_url_op.sync_detailed, _to_uuid(conversation_id))


__all__ = ["Kora"]
