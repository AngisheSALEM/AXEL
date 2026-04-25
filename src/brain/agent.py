from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel, Field
from loguru import logger
from typing import Any

# Importation locale (sera résolue via sys.path dans main.py)
try:
    from brain.memory import save_to_vault
    from hands.system_tools import list_project_files, read_project_file
except ImportError:
    from .memory import save_to_vault
    from hands.system_tools import list_project_files, read_project_file

# Configuration du modèle Ollama Local
# OllamaProvider n'existe pas directement, on utilise OpenAIProvider configuré pour Ollama
ollama_provider = OpenAIProvider(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)

local_model = OllamaModel(
    model_name='llama3.1',
    provider=ollama_provider
)

class MemorySchema(BaseModel):
    topic: str = Field(description="Le sujet principal de l'information")
    category: str = Field(description="La catégorie (ex: code, concept, rappel, erreur)")
    content: str = Field(description="Le contenu détaillé à mémoriser")

# Définition de l'Agent AXEL
axel = Agent(
    model=local_model,
    system_prompt=(
        "Tu es AXEL, un assistant OS-Copilot souverain et intelligent. "
        "Tu as accès au système de fichiers local et à une mémoire persistante. "
        "Sois précis, technique et efficace. "
        "Utilise l'outil 'memorize' pour sauvegarder des informations importantes."
    ),
)

# --- ENREGISTREMENT DES OUTILS ---

@axel.tool
def memorize(ctx: RunContext, memory_data: MemorySchema) -> str:
    """Sauvegarde une information importante dans le Vault local."""
    return save_to_vault(memory_data.topic, memory_data.category, memory_data.content)

@axel.tool
def list_files(ctx: RunContext[Any], directory: str = ".") -> list[str]:
    """Liste les fichiers dans le répertoire du projet pour exploration."""
    return list_project_files(directory)

@axel.tool
def read_file(ctx: RunContext[Any], filepath: str) -> str:
    """Lit le contenu d'un fichier source du projet."""
    return read_project_file(filepath)

logger.info("🧠 Agent AXEL configuré avec succès.")
