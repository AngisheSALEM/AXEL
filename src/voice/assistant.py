from livekit.agents import JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from loguru import logger

async def entrypoint(ctx: JobContext):
    logger.info(f"Connexion établie avec la room: {ctx.room.name}")

    # Le contexte initial d'AXEL
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "Tu es AXEL. Tu es un assistant système vocal. "
            "Tes réponses doivent être courtes, car elles sont lues à haute voix."
        ),
    )

    # Configuration de l'assistant (Lien entre Oreilles, Cerveau et Voix)
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),  # Détection de voix
        stt=openai.STT(),       # Transcription (Whisper)
        llm=openai.LLM(),       # Moteur de réponse
        tts=openai.TTS(),       # Synthèse vocale
        chat_ctx=initial_ctx,
    )

    await ctx.connect()
    assistant.start(ctx.room)
    
    await assistant.say("AXEL est en ligne. Je t'écoute.", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))