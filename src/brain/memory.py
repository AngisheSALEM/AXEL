import json
import os
from pathlib import Path
from datetime import datetime
from loguru import logger

# Chemin vers le coffre-fort de mémoire
VAULT_DIR = Path("vault/memory")

def save_to_vault(topic: str, category: str, content: str) -> str:
    """
    Sauvegarde une information importante dans le Vault sous forme de fichier JSON.
    """
    try:
        # S'assurer que le dossier existe
        VAULT_DIR.mkdir(parents=True, exist_ok=True)

        # Nettoyage du nom de fichier
        safe_topic = topic.replace(" ", "_").replace("/", "_").lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{category}_{safe_topic}_{timestamp}.json"
        filepath = VAULT_DIR / filename

        memory_data = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "category": category,
            "content": content
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(memory_data, f, indent=4, ensure_ascii=False)

        logger.success(f"💾 Mémoire sauvegardée avec succès : {filename}")
        return f"Information mémorisée dans {filename}"

    except Exception as e:
        logger.error(f"❌ Erreur lors de la sauvegarde dans le Vault : {e}")
        return f"Erreur de mémorisation : {str(e)}"
