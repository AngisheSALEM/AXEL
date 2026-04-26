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

        logger.success(f"💾 Mémoire sauvegardée : {filename}")
        return f"Information mémorisée dans {filename}"

    except Exception as e:
        logger.error(f"❌ Erreur sauvegarde Vault : {e}")
        return f"Erreur de mémorisation : {str(e)}"

def search_vault(query: str) -> str:
    """
    Recherche des informations pertinentes dans le Vault.
    """
    try:
        logger.info(f"🔍 Recherche dans le Vault : '{query}'")
        if not VAULT_DIR.exists():
            return "Le Vault est vide (aucun dossier de mémoire trouvé)."

        results = []
        query = query.lower()

        for file in VAULT_DIR.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

                # Recherche simple dans le topic et le contenu
                if query in data.get("topic", "").lower() or query in data.get("content", "").lower():
                    results.append(
                        f"--- {data.get('topic')} ({data.get('category')}) ---\n"
                        f"Date: {data.get('timestamp')}\n"
                        f"Contenu: {data.get('content')}\n"
                    )

        if not results:
            logger.warning(f"∅ Aucun résultat pour '{query}'")
            return f"Aucun souvenir trouvé pour '{query}'."

        logger.success(f"✅ {len(results)} souvenirs trouvés.")
        return "\n".join(results)

    except Exception as e:
        logger.error(f"❌ Erreur recherche Vault : {e}")
        return f"Erreur lors de la recherche : {str(e)}"
