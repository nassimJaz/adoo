from app import db

# Import all models
from app.models.utilisateur import Utilisateur
from app.models.projet import Projet
from app.models.tache import Tache
from app.models.commentaire import Commentaire
from app.models.projet_membre import ProjetMembre
from app.models.notification import Notification

__all__ = ['db', 'Utilisateur', 'Projet', 'Tache', 'Commentaire', 'ProjetMembre', 'Notification']
