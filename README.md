# 🤖 AXEL - Assistant OS-Copilot Souverain

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![Local-First](https://img.shields.io/badge/privacy-100%25%20Local-orange)

AXEL est un système OS-Copilot modulaire et local-first conçu pour offrir une assistance intelligente tout en garantissant une souveraineté totale des données.

---

## 🚀 Fonctionnalités Clés

*   **🧠 Architecture Multi-Agent :** Système hiérarchique avec un agent **MANAGER** pour la planification et un agent **CODER** pour l'exécution technique.
*   **🛠️ Intégration Système (Hands) :** Capacités étendues de manipulation de fichiers et d'exécution de commandes via le protocole **FastMCP**.
*   **🎙️ Interface Vocale (Voice) :** Pipeline vocal complet (STT/TTS/VAD) propulsé par **LiveKit** pour une interaction naturelle.
*   **💾 Mémoire Persistante (Memory) :** Système de "Vault" local utilisant du JSON pour mémoriser les contextes, les erreurs et les préférences utilisateur.
*   **🔒 Souveraineté Totale :** Toutes les opérations LLM s'exécutent localement via **Ollama**, garantissant qu'aucune donnée ne quitte votre machine.

---

## 🛠️ Stack Technique

| Secteur | Technologies |
| :--- | :--- |
| **Cerveau (Agent AI)** | PydanticAI, Ollama (Llama 3.1) |
| **Outils Système** | FastMCP, Subprocess |
| **Interface Vocale** | LiveKit Agents, Silero VAD |
| **Stockage & Mémoire** | Local JSON (Vault), Python Pathlib |
| **Logging & Obs.** | Loguru |

---

## ⚙️ Installation et Configuration

### Pré-requis

*   **Python 3.12+**
*   **Ollama** (installé et en cours d'exécution avec le modèle `llama3.1`)
*   **LiveKit Server** (optionnel pour les fonctionnalités vocales distantes)

### Démarrage Rapide

1.  **Cloner le dépôt :**
    ```bash
    git clone https://github.com/votre-compte/axel.git
    cd axel
    ```

2.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Lancer le serveur Ollama :**
    ```bash
    ollama serve
    # Dans un autre terminal
    ollama run llama3.1
    ```

4.  **Lancer AXEL :**
    ```bash
    python src/main.py
    ```

### Variables d'environnement

Créez un fichier `.env` à la racine si nécessaire (pour LiveKit ou clés API spécifiques) :

```env
# .env.example
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=votre_cle
LIVEKIT_API_SECRET=votre_secret
OLLAMA_BASE_URL=http://localhost:11434/v1
```

---

## 🏗️ Architecture

Le projet est structuré en quatre "organes" principaux :

*   **`src/brain/`** : Contient la logique des agents (Manager & Coder) et la configuration de PydanticAI.
*   **`src/hands/`** : Regroupe les outils système exposés via FastMCP.
*   **`src/voice/`** : Gère le pipeline de communication vocale LiveKit.
*   **`src/vault/`** : (Auto-généré) Stocke la mémoire persistante au format JSON.

Cette structure modulaire permet de faire évoluer chaque composant (ex: changer de modèle LLM ou ajouter des outils système) sans impacter le reste du système.

---

## 👨‍💻 Auteur

**AXEL Team**
*   GitHub : [@votre-profil](https://github.com/votre-profil)
*   Contact : axel-project@example.com
