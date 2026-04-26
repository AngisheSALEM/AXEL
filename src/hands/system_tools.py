import os
import subprocess
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

@mcp.tool()
def write_project_file(filepath: str, content: str) -> str:
    """
    Crée ou écrase un fichier dans le projet.
    """
    try:
        path = Path(filepath)

        # Sécurité de base
        if ".git" in path.parts or path.is_absolute() and not str(path).startswith(os.getcwd()):
             return "Erreur: Tentative d'écriture hors du projet ou dans un dossier protégé."

        # Création des dossiers parents si nécessaire
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"📝 Fichier écrit : {filepath}")
        return f"Succès: Fichier {filepath} mis à jour."
    except Exception as e:
        logger.error(f"Erreur write_project_file: {e}")
        return f"Erreur lors de l'écriture : {str(e)}"

@mcp.tool()
def execute_command(command: str) -> str:
    """
    Exécute une commande shell et retourne le résultat.
    """
    try:
        logger.info(f"🐚 Exécution commande : {command}")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout
        if result.stderr:
            output += f"\n--- ERREURS ---\n{result.stderr}"

        return output if output else "Commande exécutée (pas de sortie)."
    except Exception as e:
        logger.error(f"Erreur execute_command: {e}")
        return f"Erreur d'exécution : {str(e)}"

# Note: Ces outils seront injectés dans l'agent PydanticAI
