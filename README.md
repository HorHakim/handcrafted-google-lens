# Handcrafted Google Lens

Une application web qui analyse vos images à l'aide de l'IA. Prenez une photo depuis votre téléphone ou uploadez une image depuis votre ordinateur, et obtenez une description détaillée en quelques secondes.

Propulsé par le modèle de vision **Llama 4 Scout** via l'API [Groq](https://groq.com).

---

## Fonctionnalités

- Prise de photo directe depuis la caméra du smartphone
- Upload d'image depuis ordinateur (JPG, PNG, WEBP, GIF)
- Prévisualisation de l'image avant analyse
- Interface responsive — fonctionne sur mobile et desktop
- Thème sombre

---

## Installation locale

### Prérequis

- Python 3.10+
- Un compte [Groq](https://console.groq.com) (gratuit) pour obtenir une clé API

### Étapes

```bash
# 1. Cloner le dépôt
git clone <url-du-repo>
cd handcrafted-google-lens

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer la clé API
cp .env.example .env
# Éditer .env et remplacer la valeur de GROQ_API_KEY

# 4. Lancer le serveur
uvicorn app:app --reload --port 8000
```

Ouvrir `http://localhost:8000` dans votre navigateur.

---

## Utilisation en ligne de commande

Pour analyser une image locale sans serveur web :

```bash
# Placer l'image à analyser dans le répertoire du projet
cp /chemin/vers/votre/image.jpg ./image.jpg

# Lancer l'analyse
python backend.py
```

---

## Déploiement sur Railway

1. Forker/pusher ce dépôt sur GitHub
2. Créer un nouveau projet sur [Railway](https://railway.app)
3. Connecter le dépôt GitHub
4. Dans les variables de service Railway, ajouter :
   ```
   GROQ_API_KEY=votre_clé_api_groq
   ```
5. Railway détecte automatiquement Python, installe les dépendances et démarre l'application via le `Procfile`

---

## Variables d'environnement

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Clé API Groq — obligatoire |

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Python · FastAPI |
| Modèle IA | Llama 4 Scout 17B via Groq |
| Frontend | HTML · HTMX · CSS · JS vanilla |
| Déploiement | Railway |
