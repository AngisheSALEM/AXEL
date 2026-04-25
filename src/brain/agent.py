from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel # <--- Import local
from pydantic import BaseModel, Field
from .memory import save_to_vault

# Utilisation du moteur Ollama configuré sur ton Codespace
local_model = OllamaModel(model_name='llama3.1') # Ou 'phi3' selon ton choix

class MemorySchema(BaseModel):
    topic: str = Field(description="Le sujet principal")
    category: str = Field(description="La catégorie (code, concept, erreur)")
    content: str = Field(description="Le contenu détaillé")

# AXEL est maintenant propulsé par ton propre serveur
axel = Agent(
    model=local_model, 
    system_prompt=(
        "Tu es AXEL, un assistant IA souverain fonctionnant en local. "
        "Tu es précis, technique et tu as une mémoire persistante. "
        "Utilise l'outil 'memorize' pour sauvegarder les infos importantes."
    ),
)

@axel.tool
def memorize(ctx: RunContext, memory_data: MemorySchema) -> str:
    """Outil pour mémoriser des infos dans le Vault."""
    return save_to_vault(
        topic=memory_data.topic,
        category=memory_data.category,
        content=memory_data.content
    )