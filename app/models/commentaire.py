from datetime import datetime
from . import db

class Commentaire(db.Model):
    """Modèle représentant un commentaire dans un projet.
    
    Attributes:
        id (str): Identifiant unique du commentaire
        contenu (str): Contenu du commentaire
        date_creation (datetime): Date de création du commentaire
    """
    
    __tablename__ = 'commentaire'
    
    id = db.Column(db.String(36), primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    # Clés étrangères
    auteur_id = db.Column(db.String(36), db.ForeignKey('utilisateur.id'), nullable=False)
    projet_id = db.Column(db.String(36), db.ForeignKey('projet.id'), nullable=False)

    def __repr__(self):
        return f'<Commentaire {self.id}>'
