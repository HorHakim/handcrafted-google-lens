# CLAUDE.md — Mémoire développeur

## Vue d'ensemble du projet

**Handcrafted Google Lens** est une application web qui permet à l'utilisateur de prendre une photo (ou d'uploader une image) et d'en obtenir une description détaillée générée par un modèle de vision IA.

**Modèle utilisé** : `meta-llama/llama-4-scout-17b-16e-instruct` via l'API Groq.

---

## Architecture

```
handcrafted-google-lens/
├── backend.py          # Logique cœur — classe ImageAgent
├── app.py              # Serveur web FastAPI
├── static/
│   ├── index.html      # Interface HTMX (SPA statique)
│   ├── style.css       # CSS mobile-first, thème sombre
│   └── app.js          # JS vanilla — prévisualisation + événements HTMX
├── context.txt         # Prompt système envoyé au modèle
├── prompt.txt          # Prompt utilisateur envoyé avec l'image
├── requirements.txt
├── Procfile            # Entrée pour Railway
└── .env                # Non commité — contient GROQ_API_KEY
```

### Deux modes d'utilisation

| Mode | Entrée | Méthode appelée |
|------|--------|-----------------|
| CLI  | chemin fichier local | `ask_vision_model(image_path)` |
| Web  | bytes uploadés via HTTP | `ask_vision_model_bytes(image_bytes, media_type)` |

Le mode CLI utilise des chemins relatifs au CWD (`./context.txt`). Le mode Web utilise `os.path.abspath(__file__)` pour résoudre les chemins — robuste sur Railway où le CWD peut différer.

---

## Variables d'environnement

| Variable | Obligatoire | Description |
|----------|-------------|-------------|
| `GROQ_API_KEY` | Oui | Clé API Groq — obtenir sur console.groq.com |
| `PORT` | Railway seulement | Injecté automatiquement par Railway |

En local : copier `.env.example` → `.env` et renseigner la clé.
Sur Railway : définir `GROQ_API_KEY` dans les variables de service (dashboard Railway).

---

## Lancer en local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur web (avec rechargement automatique)
uvicorn app:app --reload --port 8000

# Ou utiliser le CLI directement
python backend.py
```

L'interface web est accessible sur `http://localhost:8000`.

---

## Pattern HTMX — fragments HTML

L'API `/api/analyze` retourne un **fragment HTML** (`HTMLResponse`), pas du JSON. C'est intentionnel : HTMX swap directement le fragment dans `#result-container` sans JS supplémentaire.

Les erreurs (4xx/5xx) retournent aussi un fragment HTML grâce au gestionnaire d'exceptions global dans `app.py`. Le JS dans `app.js` écoute `htmx:responseError` pour injecter manuellement ces fragments (HTMX ne swap pas sur les codes d'erreur par défaut).

**Ne pas changer ce pattern vers du JSON** sans mettre à jour `app.js` en conséquence.

---

## Modifier le comportement du modèle

- **Changer le modèle** : modifier la constante `model=` dans `backend.py` (lignes `ask_vision_model` et `ask_vision_model_bytes`)
- **Changer le prompt système** : éditer `context.txt`
- **Changer la question posée** : éditer `prompt.txt`

---

## Déploiement Railway

1. Connecter le dépôt GitHub à Railway
2. Railway détecte Python via `requirements.txt` et installe automatiquement
3. Railway utilise le `Procfile` pour démarrer : `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Définir `GROQ_API_KEY` dans les variables de service Railway
5. Le fichier `.env` n'est pas déployé (gitignore) — c'est normal

---

## Notes techniques

- `pybase64` est dans `requirements.txt` mais le code utilise `base64` de la stdlib. Pas de bug — `pybase64` est un drop-in plus rapide, mais il n'est pas importé explicitement.
- La limite de taille des uploads est 10 Mo, définie dans `app.py` (`MAX_FILE_SIZE`).
- Formats d'image acceptés : JPEG, PNG, WEBP, GIF (définis dans `ALLOWED_TYPES` dans `app.py`).
- L'instance `ImageAgent` est créée au niveau module dans `app.py` (singleton). Si `GROQ_API_KEY` est absente, l'application refuse de démarrer — comportement voulu (fail-fast).
