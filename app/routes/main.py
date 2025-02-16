from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.projet import Projet
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
    print(f"Notifications: {[n.content for n in notif_utilisateur]}")
    print("================")

    return render_template('main/accueil.html', projets_utilisateur=projets_utilisateur, taches_utilisateur=taches_utilisateur, notifications=notif_utilisateur)

@bp.route('/projets')
@login_required
def projets():
    return render_template('main/projets.html')

@bp.route('/profil')
@login_required
def profile():
    return render_template('main/profil.html')
