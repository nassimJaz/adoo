from datetime import datetime
from . import db

class Projet(db.Model):
    """Modèle représentant un projet dans le système.
    
    Attributes:
        id (str): Identifiant unique du projet
        titre (str): Titre du projet
        description (str): Description détaillée du projet
        date_creation (datetime): Date de création du projet
        date_debut (datetime): Date de début prévue du projet
        date_fin_prevue (datetime): Date de fin prévue du projet
        statut (str): État actuel du projet
    """
    
    __tablename__ = 'projet'
    
    id = db.Column(db.String(36), primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_debut = db.Column(db.DateTime)
    date_fin_prevue = db.Column(db.DateTime)
    statut = db.Column(db.String(20), default='en_cours')

    # Relations
    membres = db.relationship('ProjetMembre', back_populates='projet',
                            cascade='all, delete-orphan')
    taches = db.relationship('Tache', backref='projet',
                           cascade='all, delete-orphan')
    commentaires = db.relationship('Commentaire', backref='projet',
                                 cascade='all, delete-orphan')

    @staticmethod
    def validate_dates(date_debut, date_fin_prevue):
        """Valide que la date de début est antérieure à la date de fin."""
        if date_debut and date_fin_prevue:
            return date_debut < date_fin_prevue
        return True

    def __init__(self, *args, **kwargs):
        super(Projet, self).__init__(*args, **kwargs)
        if not self.validate_dates(self.date_debut, self.date_fin_prevue):
            raise ValueError("La date de début doit être antérieure à la date de fin prévue")

    def __repr__(self):
        return f'<Projet {self.titre}>'
