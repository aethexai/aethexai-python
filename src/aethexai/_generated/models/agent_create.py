from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.agent_create_inbound_lobby_audio_preset import AgentCreateInboundLobbyAudioPreset
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.agent_create_dynamic_variables_type_0 import AgentCreateDynamicVariablesType0
    from ..models.agent_create_metadata import AgentCreateMetadata
    from ..models.custom_guardrail import CustomGuardrail


T = TypeVar("T", bound="AgentCreate")


@_attrs_define
class AgentCreate:
    """
    Attributes:
        name (str):
        system_prompt (str):
        voice_id (str):
        background_audio_url (None | str | Unset):
        content_guardrail_enabled (bool | Unset):  Default: False.
        custom_guardrails (list[CustomGuardrail] | None | Unset):
        dialect_style (str | Unset):  Default: 'formal'.
        dynamic_variables (AgentCreateDynamicVariablesType0 | None | Unset):
        end_call_behavior (str | Unset):  Default: 'auto_detect'.
        end_call_enabled (bool | Unset):  Default: True.
        end_call_phrases (list[str] | None | Unset):
        first_message (str | Unset):  Default: ''.
        focus_guardrail_enabled (bool | Unset):  Default: True.
        frequency_penalty (float | None | Unset):
        idle_check_in_after_secs (float | None | Unset):
        inbound_lobby_audio_preset (AgentCreateInboundLobbyAudioPreset | Unset):  Default:
            AgentCreateInboundLobbyAudioPreset.AMBIENT.
        inbound_lobby_audio_url (None | str | Unset):
        inbound_lobby_enabled (bool | Unset):  Default: False.
        inbound_lobby_max_wait_seconds (int | None | Unset):  Default: 45.
        inbound_lobby_message (None | str | Unset):
        interruption_enabled (bool | Unset):  Default: True.
        language (str | Unset):  Default: 'english'.
        llm_model (str | Unset):  Default: ''.
        max_duration_seconds (int | None | Unset):  Default: 600.
        max_idle_attempts (int | None | Unset):
        max_tokens (int | None | Unset):
        metadata (AgentCreateMetadata | Unset):
        presence_penalty (float | None | Unset):
        recording_enabled (bool | Unset):  Default: True.
        response_max_sentences (int | None | Unset):
        response_min_sentences (int | None | Unset):
        script_adherence (str | Unset):  Default: 'strict'.
        silence_timeout_seconds (int | None | Unset):
        soft_timeout_message (None | str | Unset):
        soft_timeout_seconds (float | None | Unset):
        soft_timeout_use_llm (bool | Unset):  Default: False.
        temperature (float | None | Unset):
        transcription_enabled (bool | Unset):  Default: True.
        transfer_phone_number (None | str | Unset):
        turn_eagerness (None | str | Unset):
        voicemail_action (str | Unset):  Default: 'leave_message'.
        voicemail_detection_enabled (bool | Unset):  Default: False.
        voicemail_message (None | str | Unset):
    """

    name: str
    system_prompt: str
    voice_id: str
    background_audio_url: None | str | Unset = UNSET
    content_guardrail_enabled: bool | Unset = False
    custom_guardrails: list[CustomGuardrail] | None | Unset = UNSET
    dialect_style: str | Unset = "formal"
    dynamic_variables: AgentCreateDynamicVariablesType0 | None | Unset = UNSET
    end_call_behavior: str | Unset = "auto_detect"
    end_call_enabled: bool | Unset = True
    end_call_phrases: list[str] | None | Unset = UNSET
    first_message: str | Unset = ""
    focus_guardrail_enabled: bool | Unset = True
    frequency_penalty: float | None | Unset = UNSET
    idle_check_in_after_secs: float | None | Unset = UNSET
    inbound_lobby_audio_preset: AgentCreateInboundLobbyAudioPreset | Unset = (
        AgentCreateInboundLobbyAudioPreset.AMBIENT
    )
    inbound_lobby_audio_url: None | str | Unset = UNSET
    inbound_lobby_enabled: bool | Unset = False
    inbound_lobby_max_wait_seconds: int | None | Unset = 45
    inbound_lobby_message: None | str | Unset = UNSET
    interruption_enabled: bool | Unset = True
    language: str | Unset = "english"
    llm_model: str | Unset = ""
    max_duration_seconds: int | None | Unset = 600
    max_idle_attempts: int | None | Unset = UNSET
    max_tokens: int | None | Unset = UNSET
    metadata: AgentCreateMetadata | Unset = UNSET
    presence_penalty: float | None | Unset = UNSET
    recording_enabled: bool | Unset = True
    response_max_sentences: int | None | Unset = UNSET
    response_min_sentences: int | None | Unset = UNSET
    script_adherence: str | Unset = "strict"
    silence_timeout_seconds: int | None | Unset = UNSET
    soft_timeout_message: None | str | Unset = UNSET
    soft_timeout_seconds: float | None | Unset = UNSET
    soft_timeout_use_llm: bool | Unset = False
    temperature: float | None | Unset = UNSET
    transcription_enabled: bool | Unset = True
    transfer_phone_number: None | str | Unset = UNSET
    turn_eagerness: None | str | Unset = UNSET
    voicemail_action: str | Unset = "leave_message"
    voicemail_detection_enabled: bool | Unset = False
    voicemail_message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_create_dynamic_variables_type_0 import AgentCreateDynamicVariablesType0
        from ..models.agent_create_metadata import AgentCreateMetadata
        from ..models.custom_guardrail import CustomGuardrail

        name = self.name

        system_prompt = self.system_prompt

        voice_id = self.voice_id

        background_audio_url: None | str | Unset
        if isinstance(self.background_audio_url, Unset):
            background_audio_url = UNSET
        else:
            background_audio_url = self.background_audio_url

        content_guardrail_enabled = self.content_guardrail_enabled

        custom_guardrails: list[dict[str, Any]] | None | Unset
        if isinstance(self.custom_guardrails, Unset):
            custom_guardrails = UNSET
        elif isinstance(self.custom_guardrails, list):
            custom_guardrails = []
            for custom_guardrails_type_0_item_data in self.custom_guardrails:
                custom_guardrails_type_0_item = custom_guardrails_type_0_item_data.to_dict()
                custom_guardrails.append(custom_guardrails_type_0_item)

        else:
            custom_guardrails = self.custom_guardrails

        dialect_style = self.dialect_style

        dynamic_variables: dict[str, Any] | None | Unset
        if isinstance(self.dynamic_variables, Unset):
            dynamic_variables = UNSET
        elif isinstance(self.dynamic_variables, AgentCreateDynamicVariablesType0):
            dynamic_variables = self.dynamic_variables.to_dict()
        else:
            dynamic_variables = self.dynamic_variables

        end_call_behavior = self.end_call_behavior

        end_call_enabled = self.end_call_enabled

        end_call_phrases: list[str] | None | Unset
        if isinstance(self.end_call_phrases, Unset):
            end_call_phrases = UNSET
        elif isinstance(self.end_call_phrases, list):
            end_call_phrases = self.end_call_phrases

        else:
            end_call_phrases = self.end_call_phrases

        first_message = self.first_message

        focus_guardrail_enabled = self.focus_guardrail_enabled

        frequency_penalty: float | None | Unset
        if isinstance(self.frequency_penalty, Unset):
            frequency_penalty = UNSET
        else:
            frequency_penalty = self.frequency_penalty

        idle_check_in_after_secs: float | None | Unset
        if isinstance(self.idle_check_in_after_secs, Unset):
            idle_check_in_after_secs = UNSET
        else:
            idle_check_in_after_secs = self.idle_check_in_after_secs

        inbound_lobby_audio_preset: str | Unset = UNSET
        if not isinstance(self.inbound_lobby_audio_preset, Unset):
            inbound_lobby_audio_preset = self.inbound_lobby_audio_preset.value

        inbound_lobby_audio_url: None | str | Unset
        if isinstance(self.inbound_lobby_audio_url, Unset):
            inbound_lobby_audio_url = UNSET
        else:
            inbound_lobby_audio_url = self.inbound_lobby_audio_url

        inbound_lobby_enabled = self.inbound_lobby_enabled

        inbound_lobby_max_wait_seconds: int | None | Unset
        if isinstance(self.inbound_lobby_max_wait_seconds, Unset):
            inbound_lobby_max_wait_seconds = UNSET
        else:
            inbound_lobby_max_wait_seconds = self.inbound_lobby_max_wait_seconds

        inbound_lobby_message: None | str | Unset
        if isinstance(self.inbound_lobby_message, Unset):
            inbound_lobby_message = UNSET
        else:
            inbound_lobby_message = self.inbound_lobby_message

        interruption_enabled = self.interruption_enabled

        language = self.language

        llm_model = self.llm_model

        max_duration_seconds: int | None | Unset
        if isinstance(self.max_duration_seconds, Unset):
            max_duration_seconds = UNSET
        else:
            max_duration_seconds = self.max_duration_seconds

        max_idle_attempts: int | None | Unset
        if isinstance(self.max_idle_attempts, Unset):
            max_idle_attempts = UNSET
        else:
            max_idle_attempts = self.max_idle_attempts

        max_tokens: int | None | Unset
        if isinstance(self.max_tokens, Unset):
            max_tokens = UNSET
        else:
            max_tokens = self.max_tokens

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        presence_penalty: float | None | Unset
        if isinstance(self.presence_penalty, Unset):
            presence_penalty = UNSET
        else:
            presence_penalty = self.presence_penalty

        recording_enabled = self.recording_enabled

        response_max_sentences: int | None | Unset
        if isinstance(self.response_max_sentences, Unset):
            response_max_sentences = UNSET
        else:
            response_max_sentences = self.response_max_sentences

        response_min_sentences: int | None | Unset
        if isinstance(self.response_min_sentences, Unset):
            response_min_sentences = UNSET
        else:
            response_min_sentences = self.response_min_sentences

        script_adherence = self.script_adherence

        silence_timeout_seconds: int | None | Unset
        if isinstance(self.silence_timeout_seconds, Unset):
            silence_timeout_seconds = UNSET
        else:
            silence_timeout_seconds = self.silence_timeout_seconds

        soft_timeout_message: None | str | Unset
        if isinstance(self.soft_timeout_message, Unset):
            soft_timeout_message = UNSET
        else:
            soft_timeout_message = self.soft_timeout_message

        soft_timeout_seconds: float | None | Unset
        if isinstance(self.soft_timeout_seconds, Unset):
            soft_timeout_seconds = UNSET
        else:
            soft_timeout_seconds = self.soft_timeout_seconds

        soft_timeout_use_llm = self.soft_timeout_use_llm

        temperature: float | None | Unset
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        transcription_enabled = self.transcription_enabled

        transfer_phone_number: None | str | Unset
        if isinstance(self.transfer_phone_number, Unset):
            transfer_phone_number = UNSET
        else:
            transfer_phone_number = self.transfer_phone_number

        turn_eagerness: None | str | Unset
        if isinstance(self.turn_eagerness, Unset):
            turn_eagerness = UNSET
        else:
            turn_eagerness = self.turn_eagerness

        voicemail_action = self.voicemail_action

        voicemail_detection_enabled = self.voicemail_detection_enabled

        voicemail_message: None | str | Unset
        if isinstance(self.voicemail_message, Unset):
            voicemail_message = UNSET
        else:
            voicemail_message = self.voicemail_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "system_prompt": system_prompt,
                "voice_id": voice_id,
            }
        )
        if background_audio_url is not UNSET:
            field_dict["background_audio_url"] = background_audio_url
        if content_guardrail_enabled is not UNSET:
            field_dict["content_guardrail_enabled"] = content_guardrail_enabled
        if custom_guardrails is not UNSET:
            field_dict["custom_guardrails"] = custom_guardrails
        if dialect_style is not UNSET:
            field_dict["dialect_style"] = dialect_style
        if dynamic_variables is not UNSET:
            field_dict["dynamic_variables"] = dynamic_variables
        if end_call_behavior is not UNSET:
            field_dict["end_call_behavior"] = end_call_behavior
        if end_call_enabled is not UNSET:
            field_dict["end_call_enabled"] = end_call_enabled
        if end_call_phrases is not UNSET:
            field_dict["end_call_phrases"] = end_call_phrases
        if first_message is not UNSET:
            field_dict["first_message"] = first_message
        if focus_guardrail_enabled is not UNSET:
            field_dict["focus_guardrail_enabled"] = focus_guardrail_enabled
        if frequency_penalty is not UNSET:
            field_dict["frequency_penalty"] = frequency_penalty
        if idle_check_in_after_secs is not UNSET:
            field_dict["idle_check_in_after_secs"] = idle_check_in_after_secs
        if inbound_lobby_audio_preset is not UNSET:
            field_dict["inbound_lobby_audio_preset"] = inbound_lobby_audio_preset
        if inbound_lobby_audio_url is not UNSET:
            field_dict["inbound_lobby_audio_url"] = inbound_lobby_audio_url
        if inbound_lobby_enabled is not UNSET:
            field_dict["inbound_lobby_enabled"] = inbound_lobby_enabled
        if inbound_lobby_max_wait_seconds is not UNSET:
            field_dict["inbound_lobby_max_wait_seconds"] = inbound_lobby_max_wait_seconds
        if inbound_lobby_message is not UNSET:
            field_dict["inbound_lobby_message"] = inbound_lobby_message
        if interruption_enabled is not UNSET:
            field_dict["interruption_enabled"] = interruption_enabled
        if language is not UNSET:
            field_dict["language"] = language
        if llm_model is not UNSET:
            field_dict["llm_model"] = llm_model
        if max_duration_seconds is not UNSET:
            field_dict["max_duration_seconds"] = max_duration_seconds
        if max_idle_attempts is not UNSET:
            field_dict["max_idle_attempts"] = max_idle_attempts
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if presence_penalty is not UNSET:
            field_dict["presence_penalty"] = presence_penalty
        if recording_enabled is not UNSET:
            field_dict["recording_enabled"] = recording_enabled
        if response_max_sentences is not UNSET:
            field_dict["response_max_sentences"] = response_max_sentences
        if response_min_sentences is not UNSET:
            field_dict["response_min_sentences"] = response_min_sentences
        if script_adherence is not UNSET:
            field_dict["script_adherence"] = script_adherence
        if silence_timeout_seconds is not UNSET:
            field_dict["silence_timeout_seconds"] = silence_timeout_seconds
        if soft_timeout_message is not UNSET:
            field_dict["soft_timeout_message"] = soft_timeout_message
        if soft_timeout_seconds is not UNSET:
            field_dict["soft_timeout_seconds"] = soft_timeout_seconds
        if soft_timeout_use_llm is not UNSET:
            field_dict["soft_timeout_use_llm"] = soft_timeout_use_llm
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if transcription_enabled is not UNSET:
            field_dict["transcription_enabled"] = transcription_enabled
        if transfer_phone_number is not UNSET:
            field_dict["transfer_phone_number"] = transfer_phone_number
        if turn_eagerness is not UNSET:
            field_dict["turn_eagerness"] = turn_eagerness
        if voicemail_action is not UNSET:
            field_dict["voicemail_action"] = voicemail_action
        if voicemail_detection_enabled is not UNSET:
            field_dict["voicemail_detection_enabled"] = voicemail_detection_enabled
        if voicemail_message is not UNSET:
            field_dict["voicemail_message"] = voicemail_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_create_dynamic_variables_type_0 import AgentCreateDynamicVariablesType0
        from ..models.agent_create_metadata import AgentCreateMetadata
        from ..models.custom_guardrail import CustomGuardrail

        d = dict(src_dict)
        name = d.pop("name")

        system_prompt = d.pop("system_prompt")

        voice_id = d.pop("voice_id")

        def _parse_background_audio_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        background_audio_url = _parse_background_audio_url(d.pop("background_audio_url", UNSET))

        content_guardrail_enabled = d.pop("content_guardrail_enabled", UNSET)

        def _parse_custom_guardrails(data: object) -> list[CustomGuardrail] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                custom_guardrails_type_0 = []
                _custom_guardrails_type_0 = data
                for custom_guardrails_type_0_item_data in _custom_guardrails_type_0:
                    custom_guardrails_type_0_item = CustomGuardrail.from_dict(
                        custom_guardrails_type_0_item_data
                    )

                    custom_guardrails_type_0.append(custom_guardrails_type_0_item)

                return custom_guardrails_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CustomGuardrail] | None | Unset, data)

        custom_guardrails = _parse_custom_guardrails(d.pop("custom_guardrails", UNSET))

        dialect_style = d.pop("dialect_style", UNSET)

        def _parse_dynamic_variables(
            data: object,
        ) -> AgentCreateDynamicVariablesType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dynamic_variables_type_0 = AgentCreateDynamicVariablesType0.from_dict(data)

                return dynamic_variables_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AgentCreateDynamicVariablesType0 | None | Unset, data)

        dynamic_variables = _parse_dynamic_variables(d.pop("dynamic_variables", UNSET))

        end_call_behavior = d.pop("end_call_behavior", UNSET)

        end_call_enabled = d.pop("end_call_enabled", UNSET)

        def _parse_end_call_phrases(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                end_call_phrases_type_0 = cast(list[str], data)

                return end_call_phrases_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        end_call_phrases = _parse_end_call_phrases(d.pop("end_call_phrases", UNSET))

        first_message = d.pop("first_message", UNSET)

        focus_guardrail_enabled = d.pop("focus_guardrail_enabled", UNSET)

        def _parse_frequency_penalty(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        frequency_penalty = _parse_frequency_penalty(d.pop("frequency_penalty", UNSET))

        def _parse_idle_check_in_after_secs(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        idle_check_in_after_secs = _parse_idle_check_in_after_secs(
            d.pop("idle_check_in_after_secs", UNSET)
        )

        _inbound_lobby_audio_preset = d.pop("inbound_lobby_audio_preset", UNSET)
        inbound_lobby_audio_preset: AgentCreateInboundLobbyAudioPreset | Unset
        if isinstance(_inbound_lobby_audio_preset, Unset):
            inbound_lobby_audio_preset = UNSET
        else:
            inbound_lobby_audio_preset = AgentCreateInboundLobbyAudioPreset(
                _inbound_lobby_audio_preset
            )

        def _parse_inbound_lobby_audio_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        inbound_lobby_audio_url = _parse_inbound_lobby_audio_url(
            d.pop("inbound_lobby_audio_url", UNSET)
        )

        inbound_lobby_enabled = d.pop("inbound_lobby_enabled", UNSET)

        def _parse_inbound_lobby_max_wait_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        inbound_lobby_max_wait_seconds = _parse_inbound_lobby_max_wait_seconds(
            d.pop("inbound_lobby_max_wait_seconds", UNSET)
        )

        def _parse_inbound_lobby_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        inbound_lobby_message = _parse_inbound_lobby_message(d.pop("inbound_lobby_message", UNSET))

        interruption_enabled = d.pop("interruption_enabled", UNSET)

        language = d.pop("language", UNSET)

        llm_model = d.pop("llm_model", UNSET)

        def _parse_max_duration_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_duration_seconds = _parse_max_duration_seconds(d.pop("max_duration_seconds", UNSET))

        def _parse_max_idle_attempts(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_idle_attempts = _parse_max_idle_attempts(d.pop("max_idle_attempts", UNSET))

        def _parse_max_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_tokens = _parse_max_tokens(d.pop("max_tokens", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: AgentCreateMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = AgentCreateMetadata.from_dict(_metadata)

        def _parse_presence_penalty(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        presence_penalty = _parse_presence_penalty(d.pop("presence_penalty", UNSET))

        recording_enabled = d.pop("recording_enabled", UNSET)

        def _parse_response_max_sentences(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        response_max_sentences = _parse_response_max_sentences(
            d.pop("response_max_sentences", UNSET)
        )

        def _parse_response_min_sentences(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        response_min_sentences = _parse_response_min_sentences(
            d.pop("response_min_sentences", UNSET)
        )

        script_adherence = d.pop("script_adherence", UNSET)

        def _parse_silence_timeout_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        silence_timeout_seconds = _parse_silence_timeout_seconds(
            d.pop("silence_timeout_seconds", UNSET)
        )

        def _parse_soft_timeout_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        soft_timeout_message = _parse_soft_timeout_message(d.pop("soft_timeout_message", UNSET))

        def _parse_soft_timeout_seconds(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        soft_timeout_seconds = _parse_soft_timeout_seconds(d.pop("soft_timeout_seconds", UNSET))

        soft_timeout_use_llm = d.pop("soft_timeout_use_llm", UNSET)

        def _parse_temperature(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        transcription_enabled = d.pop("transcription_enabled", UNSET)

        def _parse_transfer_phone_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        transfer_phone_number = _parse_transfer_phone_number(d.pop("transfer_phone_number", UNSET))

        def _parse_turn_eagerness(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        turn_eagerness = _parse_turn_eagerness(d.pop("turn_eagerness", UNSET))

        voicemail_action = d.pop("voicemail_action", UNSET)

        voicemail_detection_enabled = d.pop("voicemail_detection_enabled", UNSET)

        def _parse_voicemail_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        voicemail_message = _parse_voicemail_message(d.pop("voicemail_message", UNSET))

        agent_create = cls(
            name=name,
            system_prompt=system_prompt,
            voice_id=voice_id,
            background_audio_url=background_audio_url,
            content_guardrail_enabled=content_guardrail_enabled,
            custom_guardrails=custom_guardrails,
            dialect_style=dialect_style,
            dynamic_variables=dynamic_variables,
            end_call_behavior=end_call_behavior,
            end_call_enabled=end_call_enabled,
            end_call_phrases=end_call_phrases,
            first_message=first_message,
            focus_guardrail_enabled=focus_guardrail_enabled,
            frequency_penalty=frequency_penalty,
            idle_check_in_after_secs=idle_check_in_after_secs,
            inbound_lobby_audio_preset=inbound_lobby_audio_preset,
            inbound_lobby_audio_url=inbound_lobby_audio_url,
            inbound_lobby_enabled=inbound_lobby_enabled,
            inbound_lobby_max_wait_seconds=inbound_lobby_max_wait_seconds,
            inbound_lobby_message=inbound_lobby_message,
            interruption_enabled=interruption_enabled,
            language=language,
            llm_model=llm_model,
            max_duration_seconds=max_duration_seconds,
            max_idle_attempts=max_idle_attempts,
            max_tokens=max_tokens,
            metadata=metadata,
            presence_penalty=presence_penalty,
            recording_enabled=recording_enabled,
            response_max_sentences=response_max_sentences,
            response_min_sentences=response_min_sentences,
            script_adherence=script_adherence,
            silence_timeout_seconds=silence_timeout_seconds,
            soft_timeout_message=soft_timeout_message,
            soft_timeout_seconds=soft_timeout_seconds,
            soft_timeout_use_llm=soft_timeout_use_llm,
            temperature=temperature,
            transcription_enabled=transcription_enabled,
            transfer_phone_number=transfer_phone_number,
            turn_eagerness=turn_eagerness,
            voicemail_action=voicemail_action,
            voicemail_detection_enabled=voicemail_detection_enabled,
            voicemail_message=voicemail_message,
        )

        agent_create.additional_properties = d
        return agent_create

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
