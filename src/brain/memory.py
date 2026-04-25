import json
import os
from pathlib import Path
from datetime import datetime
from loguru import logger

VAULT_DIR = Path("vault/memory")

def save_to_vault(topic: str, category: str, content: str) -> str:
    try:
        os.makedirs(VAULT_DIR, exist_ok=True)
        safe_topic = topic.replace(" ", "_").lower()
        filename = f"{category}_{safe_topic}.json"
        filepath = VAULT_DIR / filename
        memory_data = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "category": category,
            "content": content
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(memory_data, f, indent=4)
        logger.success(f"💾 Mémoire sauvegardée : {filename}")
        return f"Succès : '{topic}' mémorisé."
    except Exception as e:
        logger.error(f"Erreur Vault : {e}")
        return f"Erreur : {e}"
