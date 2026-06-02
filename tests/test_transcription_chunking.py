"""Edge-case tests for client-side WAV chunking / normalization.

These complement the wrapper smoke tests in ``test_kora_methods.py`` and
``test_aethexai_methods.py`` by pinning down behaviours the wrappers only
exercise loosely:

  * the exact 30s boundary (single request) vs 31s (chunked)
  * every uploaded chunk is <= the 30s chunk cap (parsed from the WAV)
  * silence-aware cuts land at/near a constructed silent gap
  * stereo / 48k inputs are normalized to canonical 24000/1/16-bit
  * graceful fall back to WAV-only behaviour when PyAV is absent

The helpers build *real* PCM WAVs so the assertions check decoded duration /
format rather than byte-count heuristics. Backend segments are empty in prod,
so merging is text-only — we assert merged text, never timestamps.
"""

from __future__ import annotations

import io
import math
import struct
import wave

import httpx
import pytest
import respx

from aethexai import AethexAI, AsyncAethexAI, Kora
from aethexai import _transcription as T
from aethexai._generated.models.body_transcribe_sync_api_v1_transcribe_post import (
    BodyTranscribeSyncApiV1TranscribePost,
)
from aethexai._generated.types import File

BASE_URL = "https://api.test.aethexai.com"
CANONICAL_RATE = 24000


def _make_wav(seconds: float, *, rate: int = CANONICAL_RATE, channels: int = 1) -> bytes:
    """A silent 16-bit WAV of the given duration / rate / channel count."""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes((b"\x00\x00" * channels) * int(seconds * rate))
    return buffer.getvalue()


def _make_wav_pcm(samples: list[int], *, rate: int = CANONICAL_RATE) -> bytes:
    """A mono 16-bit WAV built from raw int16 samples."""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"".join(struct.pack("<h", int(s)) for s in samples))
    return buffer.getvalue()


def _tone_with_gap(
    seconds: float, gap_start: float, gap_end: float, *, rate: int = CANONICAL_RATE
) -> bytes:
    """A loud sine tone with a silent region in [gap_start, gap_end)."""
    samples = []
    for i in range(int(seconds * rate)):
        sec = i / rate
        if gap_start <= sec < gap_end:
            samples.append(0)
        else:
            samples.append(int(10000 * math.sin(2 * math.pi * 200 * sec)))
    return _make_wav_pcm(samples, rate=rate)


def _wav_meta(content: bytes) -> tuple[int, int, int]:
    """Decode the WAV embedded in a multipart request body -> (channels, sampwidth, rate)."""
    blob = content[content.index(b"RIFF") :]
    with wave.open(io.BytesIO(blob)) as w:
        return w.getnchannels(), w.getsampwidth(), w.getframerate()


def _uploaded_seconds(content: bytes) -> float:
    """Decode the WAV embedded in a multipart request body -> duration in seconds."""
    blob = content[content.index(b"RIFF") :]
    return T.wav_seconds(blob) or 0.0


# ─── pure-helper boundary precision ──────────────────────────────────────────


@pytest.mark.parametrize("seconds", [25.0, 29.999, 30.0])
def test_chunks_at_or_below_cap_stay_single(seconds: float) -> None:
    """A WAV at or under the 30s chunk cap is one request."""
    chunks = T.prepare_chunks(_make_wav(seconds))
    assert chunks is not None
    assert len(chunks) == 1


@pytest.mark.parametrize("seconds", [30.5, 31.0, 45.0, 80.0])
def test_chunks_above_cap_split(seconds: float) -> None:
    """A WAV above the 30s chunk cap is split into multiple requests."""
    chunks = T.prepare_chunks(_make_wav(seconds))
    assert chunks is not None
    assert len(chunks) >= 2
    assert len(chunks) >= math.ceil(seconds / T.CHUNK_SECONDS)


@pytest.mark.parametrize("seconds", [31.0, 62.0, 95.0, 121.0])
def test_no_chunk_exceeds_cap(seconds: float) -> None:
    """No produced chunk decodes to more than the 30s cap, and chunks stay canonical."""
    chunks = T.prepare_chunks(_make_wav(seconds))
    assert chunks is not None
    for chunk in chunks:
        assert (T.wav_seconds(chunk) or 0.0) <= T.CHUNK_SECONDS + 1e-6
        with wave.open(io.BytesIO(chunk)) as w:
            assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, CANONICAL_RATE)


def test_chunk_durations_sum_to_original() -> None:
    """Hard-cut chunking is lossless: chunk durations sum back to the source length."""
    source = 70.0
    chunks = T.prepare_chunks(_make_wav(source))
    assert chunks is not None
    total = sum(T.wav_seconds(c) or 0.0 for c in chunks)
    assert total == pytest.approx(source, abs=0.05)


# ─── silence-aware seam placement ────────────────────────────────────────────


def test_silence_split_cuts_at_gap_before_boundary() -> None:
    """With a silent gap just inside the search band, the cut lands in the gap, not at 30s."""
    wav = _tone_with_gap(40.0, gap_start=28.4, gap_end=28.6)
    chunks = T.prepare_chunks(wav)
    assert chunks is not None and len(chunks) == 2
    first = T.wav_seconds(chunks[0]) or 0.0
    assert 28.4 - 0.06 <= first <= 28.6 + 0.06
    assert first < 30.0


def test_silence_split_hard_cuts_without_gap() -> None:
    """Constant-energy audio with no quiet seam falls back to a hard cut near the cap."""
    samples = [10000 if i % 2 else -10000 for i in range(int(40 * CANONICAL_RATE))]
    wav = _make_wav_pcm(samples)
    chunks = T.prepare_chunks(wav)
    assert chunks is not None and len(chunks) == 2
    first = T.wav_seconds(chunks[0]) or 0.0
    assert T.CHUNK_SECONDS - 2.1 <= first <= T.CHUNK_SECONDS


# ─── text-only seam merge over disjoint chunks ───────────────────────────────


class _Resp:
    """A minimal stand-in for a parsed transcription response."""

    def __init__(self, text: str, duration: float | None = None) -> None:
        self.text = text
        self.duration_seconds = duration


def test_merge_transcriptions_joins_and_sums_duration() -> None:
    """Text-based merge space-joins disjoint chunks and sums per-chunk durations."""
    merged = T.merge_transcriptions([_Resp("alpha beta", 12.0), _Resp("gamma delta", 8.0)])
    assert merged.text == "alpha beta gamma delta"
    assert merged.duration_seconds == 20.0


def test_merge_transcriptions_skips_empty_chunks() -> None:
    """Empty / whitespace chunk texts are dropped before joining."""
    merged = T.merge_transcriptions([_Resp("alpha"), _Resp("  "), _Resp("beta")])
    assert merged.text == "alpha beta"


# ─── wrapper: exact 30s -> single request, 31s -> chunked ────────────────────


def _sync_body(data: bytes) -> BodyTranscribeSyncApiV1TranscribePost:
    """A sync-transcribe body wrapping raw WAV bytes."""
    return BodyTranscribeSyncApiV1TranscribePost(
        file=File(payload=io.BytesIO(data), file_name="a.wav", mime_type="audio/wav"),
        language="english",
    )


@respx.mock
def test_transcribe_audio_exactly_30s_single_request() -> None:
    """A WAV of exactly 30s goes out as one request."""
    client = AethexAI(api_key="ae_live_test", base_url=BASE_URL)
    route = respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        return_value=httpx.Response(200, json={"id": "t1", "text": "ok"})
    )
    try:
        client.transcribe_audio(body=_sync_body(_make_wav(30.0)))
    finally:
        client.close()
    assert route.call_count == 1
    assert _uploaded_seconds(route.calls.last.request.content) == pytest.approx(30.0, abs=0.05)


@respx.mock
def test_transcribe_audio_31s_chunks() -> None:
    """A WAV just over the cap is split, and every uploaded chunk is <= 30s."""
    client = AethexAI(api_key="ae_live_test", base_url=BASE_URL)
    route = respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        side_effect=[
            httpx.Response(200, json={"id": "t1", "text": "alpha"}),
            httpx.Response(200, json={"id": "t2", "text": "beta"}),
        ]
    )
    try:
        result = client.transcribe_audio(body=_sync_body(_make_wav(31.0)))
    finally:
        client.close()
    assert route.call_count == 2
    assert result.text == "alpha beta"
    for call in route.calls:
        assert _uploaded_seconds(call.request.content) <= T.CHUNK_SECONDS + 0.05


@respx.mock
def test_kora_uploaded_chunks_never_exceed_cap() -> None:
    """Every chunk Kora uploads for a long WAV decodes to <= 30s."""
    kora = Kora(BASE_URL, "ae_live_kora_test")
    route = respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        side_effect=[httpx.Response(200, json={"id": f"t{i}", "text": f"w{i}"}) for i in range(8)]
    )
    try:
        kora.transcribe(_make_wav(95.0), mime_type="audio/wav")
    finally:
        kora.close()
    assert route.call_count >= math.ceil(95.0 / T.CHUNK_SECONDS)
    for call in route.calls:
        seconds = _uploaded_seconds(call.request.content)
        assert seconds <= T.CHUNK_SECONDS + 0.05
        assert _wav_meta(call.request.content) == (1, 2, CANONICAL_RATE)


# ─── wrapper: format conversion (stereo / 48k) requires PyAV ─────────────────


@respx.mock
def test_kora_stereo_48k_normalized_and_chunked() -> None:
    """A stereo 48k WAV is normalized to canonical mono/24k and chunked under the cap."""
    pytest.importorskip("av")
    kora = Kora(BASE_URL, "ae_live_kora_test")
    route = respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        side_effect=[httpx.Response(200, json={"id": f"t{i}", "text": f"w{i}"}) for i in range(6)]
    )
    try:
        kora.transcribe(_make_wav(65.0, rate=48000, channels=2), mime_type="audio/wav")
    finally:
        kora.close()
    assert route.call_count >= math.ceil(65.0 / T.CHUNK_SECONDS)
    for call in route.calls:
        assert _wav_meta(call.request.content) == (1, 2, CANONICAL_RATE)
        assert _uploaded_seconds(call.request.content) <= T.CHUNK_SECONDS + 0.05


@respx.mock
def test_transcribe_audio_mono_8k_resampled_to_canonical() -> None:
    """A short off-rate mono WAV is normalized to the canonical 24000 Hz mono 16-bit shape via PyAV."""
    pytest.importorskip("av")
    client = AethexAI(api_key="ae_live_test", base_url=BASE_URL)
    route = respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        return_value=httpx.Response(200, json={"id": "t1", "text": "ok"})
    )
    try:
        client.transcribe_audio(body=_sync_body(_make_wav(5.0, rate=8000)))
    finally:
        client.close()
    assert route.call_count == 1
    assert _wav_meta(route.calls.last.request.content) == (1, 2, CANONICAL_RATE)


# ─── wrapper: graceful fallback when PyAV is unavailable ─────────────────────


@respx.mock
def test_stereo_sent_raw_when_av_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without PyAV a stereo WAV can't be normalized, so it is sent unchunked as-is."""
    monkeypatch.setattr("aethexai._transcription.av", None, raising=False)
    client = AethexAI(api_key="ae_live_test", base_url=BASE_URL)
    route = respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        return_value=httpx.Response(200, json={"id": "t1", "text": "raw"})
    )
    stereo = _make_wav(40.0, rate=48000, channels=2)
    try:
        result = client.transcribe_audio(body=_sync_body(stereo))
    finally:
        client.close()
    assert route.call_count == 1
    assert result.text == "raw"
    assert _wav_meta(route.calls.last.request.content) == (2, 2, 48000)


@respx.mock
def test_mono_canonical_wav_still_chunks_when_av_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without PyAV a canonical mono WAV still chunks via the stdlib ``wave`` path."""
    monkeypatch.setattr("aethexai._transcription.av", None, raising=False)
    client = AethexAI(api_key="ae_live_test", base_url=BASE_URL)
    route = respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        side_effect=[
            httpx.Response(200, json={"id": "t1", "text": "alpha"}),
            httpx.Response(200, json={"id": "t2", "text": "beta"}),
            httpx.Response(200, json={"id": "t3", "text": "gamma"}),
        ]
    )
    try:
        result = client.transcribe_audio(body=_sync_body(_make_wav(80.0)))
    finally:
        client.close()
    assert route.call_count == 3
    assert result.text == "alpha beta gamma"
    for call in route.calls:
        assert _uploaded_seconds(call.request.content) <= T.CHUNK_SECONDS + 0.05


# ─── sync/async parity on the new format + boundary paths ────────────────────


@respx.mock
async def test_parity_exactly_30s_single_request() -> None:
    """Sync and async agree that a 30s WAV is one request returning identical text."""
    sync_client = AethexAI(api_key="ae_live_test", base_url=BASE_URL)
    async_client = AsyncAethexAI(api_key="ae_live_test", base_url=BASE_URL)
    respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        return_value=httpx.Response(200, json={"id": "t1", "text": "ok"})
    )
    try:
        sync_out = sync_client.transcribe_audio(body=_sync_body(_make_wav(30.0)))
        async_out = await async_client.transcribe_audio(body=_sync_body(_make_wav(30.0)))
    finally:
        sync_client.close()
        await async_client.close()
    assert sync_out.text == async_out.text == "ok"


@respx.mock
async def test_parity_stereo_sent_raw_when_av_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sync and async both fall back to sending stereo raw when PyAV is absent."""
    monkeypatch.setattr("aethexai._transcription.av", None, raising=False)
    sync_client = AethexAI(api_key="ae_live_test", base_url=BASE_URL)
    async_client = AsyncAethexAI(api_key="ae_live_test", base_url=BASE_URL)
    route = respx.post(f"{BASE_URL}/api/v1/transcribe").mock(
        return_value=httpx.Response(200, json={"id": "t1", "text": "raw"})
    )
    stereo = _make_wav(40.0, rate=48000, channels=2)
    try:
        sync_out = sync_client.transcribe_audio(body=_sync_body(stereo))
        async_out = await async_client.transcribe_audio(body=_sync_body(stereo))
    finally:
        sync_client.close()
        await async_client.close()
    assert sync_out.text == async_out.text == "raw"
    assert route.call_count == 2
    for call in route.calls:
        assert _wav_meta(call.request.content) == (2, 2, 48000)
