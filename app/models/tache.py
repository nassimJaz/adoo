from datetime import datetime
from . import db

class Tache(db.Model):
    """Modèle représentant une tâche dans un projet.
    
    Attributes:
        id (str): Identifiant unique de la tâche
        titre (str): Titre de la tâche
        description (str): Description détaillée de la tâche
        date_creation (datetime): Date de création de la tâche
        date_echeance (datetime): Date d'échéance de la tâche
        priorite (str): Niveau de priorité de la tâche
        statut (str): État actuel de la tâche
    """
    
    __tablename__ = 'tache'
    
    id = db.Column(db.String(36), primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_echeance = db.Column(db.DateTime)
    priorite = db.Column(db.String(20), default='normale')
    statut = db.Column(db.String(20), default='a_faire')

    # Clés étrangères
    projet_id = db.Column(db.String(36), db.ForeignKey('projet.id'), nullable=False)
    responsable_id = db.Column(db.String(36), db.ForeignKey('utilisateur.id'))

    def __repr__(self):
        return f'<Tache {self.titre}>'
