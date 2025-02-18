from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db

class Utilisateur(db.Model, UserMixin):
    """Modèle représentant un utilisateur dans le système.
    
    Attributs:
        id (str): Identifiant unique de l'utilisateur
        email (str): Adresse email unique de l'utilisateur
        mot_de_passe (str): Mot de passe hashé de l'utilisateur
        nom (str): Nom de famille de l'utilisateur
        prenom (str): Prénom de l'utilisateur
        date_inscription (datetime): Date de création du compte
    """
    
    __tablename__ = 'utilisateur'
    
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    mot_de_passe = db.Column(db.String(128), nullable=False)
    nom = db.Column(db.String(64), nullable=False)
    prenom = db.Column(db.String(64), nullable=False)
    a_propos = db.Column(db.Text, default = '')
    preferences_notif = db.Column(db.String(20), default = 'Application')
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    projets = db.relationship('ProjetMembre', back_populates='utilisateur',cascade='all, delete-orphan')
    commentaires = db.relationship('Commentaire', backref='auteur', cascade='all, delete-orphan')
    taches_assignees = db.relationship('Tache', backref='responsable', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='recipient', lazy='dynamic')

    def set_password(self, password):
        """Hash et enregistre le mot de passe de l'utilisateur."""
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie si le mot de passe fourni correspond au hash stocké."""
        return check_password_hash(self.mot_de_passe, password)

    def get_id(self):
        """Requis par Flask-Login."""
        return str(self.id)

    def __repr__(self):
        return f'<Utilisateur {self.email}>'
