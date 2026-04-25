import os
import sys
import asyncio
import httpx
from loguru import logger
from pathlib import Path

# --- RESOLUTION DES IMPORTS ---
# Ajout du dossier 'src' au path pour permettre les imports absolus
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))
sys.path.append(str(current_dir.parent))

try:
    from brain.agent import axel
except ImportError as e:
    logger.error(f"❌ Erreur d'importation : {e}")
    sys.exit(1)

async def check_ollama():
    """Vérifie si le serveur Ollama est accessible."""
    url = "http://localhost:11434/api/tags"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=2.0)
            if response.status_code == 200:
                logger.success("✅ Serveur Ollama détecté et opérationnel.")
                return True
    except Exception:
        pass

    logger.warning("⚠️ Ollama n'est pas détecté sur http://localhost:11434")
    logger.info("👉 Assurez-vous qu'Ollama est lancé ('ollama serve')")
    return False

async def main():
    logger.info("🚀 Démarrage du système AXEL OS-Copilot...")

    # 1. Vérification de l'environnement
    ollama_ready = await check_ollama()

    # 2. Simulation d'une tâche (Brain + Hands + Memory)
    if ollama_ready:
        print("\n" + "="*50)
        print("🤖 TEST DE L'AGENT AXEL")
        print("="*50)

        prompt = (
            "Analyse le fichier 'src/brain/memory.py', "
            "résume ce qu'il fait et mémorise ce résumé dans la catégorie 'architecture'."
        )

        logger.info(f"Utilisateur: {prompt}")

        try:
            # L'agent va utiliser read_project_file puis save_to_vault
            result = await axel.run(prompt)
            print(f"\n🤖 AXEL : {result.data}")
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de l'agent : {e}")
    else:
        logger.error("❌ Impossible de lancer l'agent sans Ollama.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Arrêt de AXEL...")
