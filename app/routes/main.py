from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from app import db

from app.models.projet import Projet
from app.models.projet_membre import ProjetMembre
from app.models.tache import Tache

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/accueil')
@login_required
def accueil():
    
    projets_utilisateur = [membre_projet.projet for membre_projet in current_user.projets] # Projets de l'utilisateur courant
    taches_utilisateur = Tache.query.filter_by(responsable_id=current_user.id).all() # Taches de l'utilisateur courant
    notif_utilisateur = [notifUser for notifUser in current_user.notifications] 

    

    # Debug prints
    print("=== DEBUG INFO ===")
    print(f"Tâches de l'utilisateur: {[t.titre for t in taches_utilisateur]}")
    print(f"Projets de l'utilisateur: {[p.titre for p in projets_utilisateur]}")
    print(f"Notifications: {[n.contenu for n in notif_utilisateur]}")
    print("================")

    return render_template('main/accueil.html', projets_utilisateur=projets_utilisateur, taches_utilisateur=taches_utilisateur, notifications=notif_utilisateur)

@bp.route('/projets/creer')
@login_required
def creer_projet():
    if request.method == 'POST':
        titre = request.form.get('titre')
        objectifs = request.form.get('objectifs')
        description = request.form.get('description')
        date_debut = request.form.get('date_debut')
        date_fin_prevue = request.form.get('date_fin_prevue')

        # Validation des dates
        if not Projet.validate_dates(date_debut, date_fin_prevue):
            flash('La date de début doit être antérieure à la date de fin prévue.', 'error')
            return redirect(url_for('main.creer_projet'))

        # Création du projet
        id_projet = len(Projet.query.all()) +1
        new_projet = Projet(id=id_projet, titre=titre, objectifs=objectifs, description=description, date_debut=date_debut, date_fin_prevue=date_fin_prevue)
        db.session.add(new_projet)
        db.session.commit()

        # Ajout de l'utilisateur comme membre du projet
        new_membre = ProjetMembre(utilisateur_id=current_user.id, projet_id=new_projet.id, role='chef_projet')
        db.session.add(new_membre)
        db.session.commit()

        flash('Projet créé avec succès !', 'success')
        return redirect(url_for('main.accueil'))

    return render_template('main/creer_projet.html')

@bp.route('/projets')
@login_required
def projets():
    return render_template('main/projets.html')

@bp.route('/profil')
@login_required
def profil():
    return render_template('main/profil.html')
