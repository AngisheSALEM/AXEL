import os
from mcp.server.fastmcp import FastMCP
from loguru import logger
from pathlib import Path

# Création du serveur FastMCP
mcp = FastMCP("AXEL-System-Tools")

@mcp.tool()
def list_project_files(directory: str = ".") -> list[str]:
    """
    Liste les fichiers dans le répertoire du projet pour exploration.
    """
    try:
        files = []
        for root, _, filenames in os.walk(directory):
            # Ignorer les dossiers cachés et les environnements virtuels
            if ".git" in root or ".venv" in root or "__pycache__" in root:
                continue
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files
    except Exception as e:
        logger.error(f"Erreur list_project_files: {e}")
        return [f"Erreur: {str(e)}"]

@mcp.tool()
def read_project_file(filepath: str) -> str:
    """
    Lit le contenu d'un fichier source du projet.
    """
    try:
        path = Path(filepath)
        if not path.exists():
            return f"Erreur: Le fichier {filepath} n'existe pas."

        # Sécurité : Limiter la lecture au répertoire du projet
        # (Optionnel selon les besoins de souveraineté)

        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Erreur read_project_file: {e}")
        return f"Erreur: Impossible de lire le fichier - {str(e)}"

# Note: Ces outils seront injectés dans l'agent PydanticAI
