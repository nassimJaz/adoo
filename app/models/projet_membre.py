from datetime import datetime
from . import db

class ProjetMembre(db.Model):
    """Modèle représentant l'association entre un utilisateur et un projet.
    
    Attributs:
        id_projet_membre (str): ID du lien entre un projet et un membre
        utilisateur_id (str): ID de l'utilisateur
        projet_id (str): ID du projet
        role (str): Rôle de l'utilisateur dans le projet
        date_ajout (datetime): Date d'ajout au projet
    """
    
    __tablename__ = 'projet_membre'
    
    id_projet_membre = db.Column(db.String(36), primary_key=True)
    projet_id = db.Column(db.String(36), db.ForeignKey('projet.id'))
    utilisateur_id = db.Column(db.String(36), db.ForeignKey('utilisateur.id'))
    createur_id = db.Column(db.String(36))
    role = db.Column(db.String(20), default='Lecteur')
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    utilisateur = db.relationship('Utilisateur', back_populates='projets')
    projet = db.relationship('Projet', back_populates='membres')

    def __repr__(self):
        return f'<ProjetMembre {self.utilisateur_id} {self.projet_id}>'
