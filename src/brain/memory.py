import json
import os
from pathlib import Path
from datetime import datetime
from loguru import logger

# On pointe vers ton Vault à la racine du projet
VAULT_DIR = Path("vault/memory")

def save_to_vault(topic: str, category: str, content: str) -> str:
    """
    Fonction appelée par AXEL pour mémoriser une information ou une technique.
    """
    try:
        # Création du nom de fichier propre
        safe_topic = topic.replace(" ", "_").lower()
        filename = f"{category}_{safe_topic}.json"
        filepath = VAULT_DIR / filename

        memory_data = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "category": category,
            "content": content
        }

        # Sauvegarde physique dans le Vault
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(memory_data, f, indent=4)
        
        logger.success(f"💾 Mémoire sauvegardée dans le Vault : {filename}")
        return f"Succès : L'information sur '{topic}' a été gravée dans le Vault."
    
    except Exception as e:
        logger.error(f"Erreur d'écriture dans le Vault : {e}")
        return f"Erreur de mémorisation : {e}"