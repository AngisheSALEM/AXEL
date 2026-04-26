from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel, Field
from loguru import logger
from typing import Any

# Importation locale (sera résolue via sys.path dans main.py)
try:
    from brain.memory import save_to_vault, search_vault
    from hands.system_tools import list_project_files, read_project_file, write_project_file, execute_command
except ImportError:
    from .memory import save_to_vault, search_vault
    from hands.system_tools import list_project_files, read_project_file, write_project_file, execute_command

# Configuration du modèle Ollama Local
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

# --- AGENT CODER ---
coder_agent = Agent(
    model=local_model,
    system_prompt=(
        "Tu es l'agent CODER d'AXEL. Ton rôle est l'exécution technique. "
        "Tu peux lire, écrire des fichiers et exécuter des commandes système. "
        "Sois extrêmement rigoureux sur la syntaxe et la sécurité."
    ),
)

@coder_agent.tool
def list_files_coder(ctx: RunContext[Any], directory: str = ".") -> list[str]:
    """Liste les fichiers du projet."""
    return list_project_files(directory)

@coder_agent.tool
def read_file_coder(ctx: RunContext[Any], filepath: str) -> str:
    """Lit un fichier du projet."""
    return read_project_file(filepath)

@coder_agent.tool
def write_file_coder(ctx: RunContext[Any], filepath: str, content: str) -> str:
    """Écrit ou modifie un fichier du projet."""
    return write_project_file(filepath, content)

@coder_agent.tool
def execute_shell(ctx: RunContext[Any], command: str) -> str:
    """Exécute une commande shell."""
    return execute_command(command)

# --- AGENT MANAGER (SUPERVISEUR) ---
manager_agent = Agent(
    model=local_model,
    system_prompt=(
        "Tu es le MANAGER d'AXEL, l'intelligence centrale. "
        "Ton rôle est d'analyser la demande, de chercher dans ta mémoire (Vault), "
        "de planifier et de déléguer les tâches techniques à l'agent CODER. "
        "AVANT DE RÉPONDRE 'JE NE SAIS PAS', UTILISE TOUJOURS 'search_memory'. "
        "Une fois qu'une action est accomplie, n'oublie pas de la mémoriser via 'memorize'."
    ),
)

@manager_agent.tool
def search_memory(ctx: RunContext[Any], query: str) -> str:
    """Cherche dans les souvenirs passés d'AXEL (le Vault)."""
    return search_vault(query)

@manager_agent.tool
def memorize(ctx: RunContext, memory_data: MemorySchema) -> str:
    """Sauvegarde une information importante dans le Vault local."""
    return save_to_vault(memory_data.topic, memory_data.category, memory_data.content)

@manager_agent.tool
async def delegate_to_coder(ctx: RunContext[Any], prompt: str) -> str:
    """Délègue une tâche technique (lecture, écriture, commande) au CODER."""
    logger.info(f"👨‍✈️ Manager -> Coder : {prompt}")
    # On passe l'historique des messages pour garder le contexte si nécessaire
    result = await coder_agent.run(prompt, message_history=ctx.messages)
    return result.data

@manager_agent.tool
def list_files_manager(ctx: RunContext[Any], directory: str = ".") -> list[str]:
    """Liste les fichiers du projet (pour analyse)."""
    return list_project_files(directory)

@manager_agent.tool
def read_file_manager(ctx: RunContext[Any], filepath: str) -> str:
    """Lit un fichier du projet (pour analyse)."""
    return read_project_file(filepath)

# AXEL est maintenant l'alias du manager pour l'extérieur
axel = manager_agent

logger.info("🧠 Agent AXEL configuré avec succès.")
