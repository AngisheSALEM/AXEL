import asyncio
from livekit.agents import JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import silero, openai
from loguru import logger

# Note: Pour une souveraineté totale, STT et TTS devraient être remplacés par
# des plugins utilisant des modèles locaux (ex: Deepgram avec local engine,
# ou Whisper local). Pour ce squelette, nous utilisons les abstractions
# de LiveKit qui permettent de switcher facilement.

async def entrypoint(ctx: JobContext):
    """
    Point d'entrée pour le pipeline vocal AXEL avec LiveKit.
    Configuration orientée LOCAL-FIRST.
    """
    logger.info(f"🎙️ AXEL Voice: Connexion à la room {ctx.room.name}")

    # Contexte initial spécifique à la voix
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "Tu es AXEL, l'interface vocale d'un assistant système souverain. "
            "Réponds de manière concise. Ton intelligence est locale."
        ),
    )

    # Configuration de l'assistant Vocal
    # VAD (Détection d'activité vocale) est déjà local avec Silero.
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),

        # En production hors-ligne, on utiliserait des versions locales de STT/TTS
        # Ex: livekit-plugins-whisper (local) et livekit-plugins-piper (local TTS)
        stt=openai.STT(), # Placeholder Switchable
        tts=openai.TTS(), # Placeholder Switchable

        # Le LLM peut être relié à notre agent PydanticAI (local via Ollama)
        llm=openai.LLM(), # Placeholder Switchable

        chat_ctx=initial_ctx,
    )

    await ctx.connect()
    assistant.start(ctx.room)
    
    await assistant.say("AXEL Voice activé. Je vous écoute.", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
