from datetime import datetime
from . import db

class ProjetMembre(db.Model):
    """Modèle représentant l'association entre un utilisateur et un projet.
    
    Attributes:
        utilisateur_id (str): ID de l'utilisateur
        projet_id (str): ID du projet
        role (str): Rôle de l'utilisateur dans le projet
        date_ajout (datetime): Date d'ajout au projet
    """
    
    __tablename__ = 'projet_membre'
    
    utilisateur_id = db.Column(db.String(36), db.ForeignKey('utilisateur.id'), primary_key=True)
    projet_id = db.Column(db.String(36), db.ForeignKey('projet.id'), primary_key=True)
    role = db.Column(db.String(20), default='membre')
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    utilisateur = db.relationship('Utilisateur', back_populates='projets')
    projet = db.relationship('Projet', back_populates='membres')

    def __repr__(self):
        return f'<ProjetMembre {self.utilisateur_id} {self.projet_id}>'
