"""Realtime voice module (WebRTC Conversation).

Requires the optional ``[realtime]`` extra::

    pip install aethexai[realtime]

The WebSocket-based ``TranscribeStream`` and ``VoiceStream`` clients were
removed in 0.3.0 because the underlying server routes are explicitly
deferred to v2 (AET-1364 and AET-1363). Use ``client.transcribe_audio()`` /
``client.transcribe_audio_async()`` for transcription, and Twilio or
WebRTC for voice agents.
"""

try:
    from aethexai.realtime.conversation import Conversation, ConversationCallbacks
except ImportError:
    pass

__all__ = ["Conversation", "ConversationCallbacks"]
