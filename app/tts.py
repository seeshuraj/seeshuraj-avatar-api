"""
Azure Neural TTS — returns base64-encoded WAV audio.
Falls back to empty string if Azure credentials are missing.
"""
import base64
from .config import settings


def synthesise(text: str) -> str:
    """Returns base64-encoded WAV bytes, or empty string on failure."""
    if not settings.SPEECH_KEY or not settings.SPEECH_REGION:
        return ""

    try:
        import azure.cognitiveservices.speech as speechsdk

        speech_config = speechsdk.SpeechConfig(
            subscription=settings.SPEECH_KEY,
            region=settings.SPEECH_REGION,
        )
        speech_config.speech_synthesis_voice_name = settings.SPEECH_VOICE
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        )

        synthesiser = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=None,
        )

        result = synthesiser.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return base64.b64encode(result.audio_data).decode("utf-8")
        return ""
    except Exception:
        return ""
