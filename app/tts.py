"""
Azure Neural TTS — returns base64-encoded WAV audio.
Falls back to empty string if credentials are missing.
"""

import base64
import asyncio
from app.config import settings


async def synthesise(text: str) -> str:
    """Convert text to speech via Azure and return base64-encoded WAV."""
    if not settings.speech_key or not settings.speech_region:
        return ""

    try:
        import azure.cognitiveservices.speech as speechsdk
    except ImportError:
        return ""

    speech_config = speechsdk.SpeechConfig(
        subscription=settings.speech_key,
        region=settings.speech_region,
    )
    speech_config.speech_synthesis_voice_name = settings.speech_voice
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
    )

    # Use pull audio output stream to capture bytes
    stream = speechsdk.audio.PullAudioOutputStream()
    audio_config = speechsdk.audio.AudioOutputConfig(stream=stream)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, lambda: synthesizer.speak_text_async(text).get()
    )

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
        return base64.b64encode(audio_data).decode("utf-8")

    return ""
