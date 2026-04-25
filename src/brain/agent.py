from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic import BaseModel, Field
from .memory import save_to_vault

local_model = OllamaModel(model_name='llama3.1')

class MemorySchema(BaseModel):
    topic: str = Field(description="Sujet")
    category: str = Field(description="Catégorie (code, concept, erreur)")
    content: str = Field(description="Contenu")

axel = Agent(
    model=local_model, 
    system_prompt="Tu es AXEL, assistant système local. Utilise 'memorize' pour le Vault.",
)

@axel.tool
def memorize(ctx: RunContext, memory_data: MemorySchema) -> str:
    return save_to_vault(memory_data.topic, memory_data.category, memory_data.content)
