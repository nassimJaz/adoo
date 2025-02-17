from datetime import datetime
from app import db

class Notification(db.Model):
    """Modèle une notification envoyée à un utilisateur.
    
    Attributs:
        id (str): Identifiant unique de la notification
        user_id (str): Identifiant de l'utilisateur destinataire (peut être null)
        project_id (str): Identifiant du projet concerné (peut être null)
        type (str): Type de notification (mail ou application)
        contenu (str): Contenu de la notification
        created_at (datetime): Date de création de la notification
    """

    __tablename__ = 'notifications'
    
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('utilisateur.id'), nullable=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projet.id'), nullable=True) 
    type = db.Column(db.String(50), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
