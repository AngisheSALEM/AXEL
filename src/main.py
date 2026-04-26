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
    logger.info("🚀 Démarrage du système AXEL - Phase 2 (Opérateur Automatisé)")

    # 1. Vérification de l'environnement
    ollama_ready = await check_ollama()

    if not ollama_ready:
        logger.error("❌ Impossible de lancer AXEL sans Ollama.")
        return

    # 2. Simulation d'une tâche complexe (Multi-Agent + Système + Mémoire)
    print("\n" + "═"*50)
    print("🤖 AXEL : INTERFACE MANAGER ACTIVÉE")
    print("═"*50)

    prompt = (
        "AXEL, analyse mon fichier 'src/main.py', trouve une optimisation "
        "pour la gestion des erreurs, écris le correctif, et mémorise cette action."
    )

    logger.info(f"👤 Utilisateur : {prompt}")

    try:
        # L'agent MANAGER va piloter la mission
        result = await axel.run(prompt)

        print("\n" + "═"*50)
        print(f"✅ MISSION ACCOMPLIE : {result.data}")
        print("═"*50)

    except Exception as e:
        logger.error(f"💥 Erreur critique : {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Arrêt de AXEL...")
