
# Installation du projet

1. Cloner le projet
```bash
git clone <votre-repo>
cd <votre-projet>
```

2. Créer et activer un environnement virtuel
```bash
python -m venv venv

source venv/bin/activate  # Sur Linux/Mac
# ou
source venv/Scripts/activate # Windows avec Git Bash

venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

6. Initialiser la base de données (déjà existante)
```bash
flask db upgrade
```

7. Lancer l'application
```bash
python run.py
```

# Accès
- URL: http://localhost:5000


