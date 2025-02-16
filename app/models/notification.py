from datetime import datetime
from app import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('utilisateur.id'), nullable=False)  # Changé en 'utilisateur' et String(36)
    project_id = db.Column(db.String(36), db.ForeignKey('projet.id'))  # Changé en 'projet' et String(36)
    type = db.Column(db.String(50), nullable=False) #type de notif (mail ou sur l'appli)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
