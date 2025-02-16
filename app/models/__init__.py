from app import db  # Import db from app package instead of creating a new instance

# Import all models
from app.models.utilisateur import Utilisateur
from app.models.projet import Projet
from app.models.tache import Tache
from app.models.commentaire import Commentaire
from app.models.projet_membre import ProjetMembre

__all__ = ['db', 'Utilisateur', 'Projet', 'Tache', 'Commentaire', 'ProjetMembre']
