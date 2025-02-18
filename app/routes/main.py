from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from app import db

from app.models.projet import Projet
from app.models.projet_membre import ProjetMembre
from app.models.tache import Tache
from app.models.utilisateur import Utilisateur

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/accueil')
@login_required
def accueil():
    
    projets_utilisateur = [membre_projet.projet for membre_projet in current_user.projets] # Projets de l'utilisateur courant
    roles_utilisateur = [role_projet.role for role_projet in current_user.projets] # Roles de l'utilisateur courant accordés aux projets
    taches_utilisateur = Tache.query.filter_by(responsable_id=current_user.id).all() # Taches de l'utilisateur courant
    notif_utilisateur = [notifUser for notifUser in current_user.notifications] 

    return render_template('main/accueil.html', projets_utilisateur=projets_utilisateur, roles_utilisateur=roles_utilisateur, taches_utilisateur=taches_utilisateur, notifications=notif_utilisateur)

@bp.route('/projets/creer', methods=['GET', 'POST'])
@login_required
def creer_projet():
    if request.method == 'POST':
        titre = request.form.get('titre')
        objectifs = request.form.get('objectifs')
        description = request.form.get('description')
        
        date_debut = datetime.strptime(request.form.get('date_debut'), '%Y-%m-%d')
        date_fin_prevue = datetime.strptime(request.form.get('date_fin_prevue'), '%Y-%m-%d')

        # Validation des dates
        if not Projet.validate_dates(date_debut, date_fin_prevue):
            flash('La date de début doit être antérieure à la date de fin prévue.', 'error')
            return redirect(url_for('main.creer_projet'))

        try:
            # Création du projet
            id_projet = f"projet_{len(Projet.query.all()) +1}"
            new_projet = Projet(id=id_projet, titre=titre, objectifs=objectifs, description=description, date_debut=date_debut, date_fin_prevue=date_fin_prevue)
            db.session.add(new_projet)
            db.session.commit()

            # Ajout de l'utilisateur comme membre du projet
            id_projet_membre = f"projet_membre_{len(ProjetMembre.query.all()) +1}"
            new_membre = ProjetMembre(id_projet_membre=id_projet_membre, projet_id=new_projet.id, utilisateur_id=current_user.id, role='Administrateur')
            db.session.add(new_membre)
            db.session.commit()

            flash('Projet créé avec succès !', 'success')
            return redirect(url_for('main.accueil'))

        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la création du projet: {e}")
            flash('Une erreur est survenue lors de la création du projet.', 'error')
        return redirect(url_for('main.creer_projet'))

    return render_template('main/creer_projet.html')

@bp.route('/projets')
@login_required
def projets():
    # affiche tout les projets de l'application
    projets = Projet.query.all()
    return render_template('main/projets.html', projets=projets)

@bp.route('/projets/<string:id_projet>')
@login_required
def projet_detaille(id_projet):
    projet = Projet.query.get(id_projet)
    membres = ProjetMembre.query.filter_by(projet_id=projet.id).all()
    membres_id = [membre.utilisateur_id for membre in membres]
    taches = Tache.query.filter_by(projet_id = id_projet).all()

    list_role_utilisateur = [membre.role for membre in membres if membre.utilisateur_id == current_user.id]
    if len(list_role_utilisateur) != 0:
        role_utilisateur = list_role_utilisateur[0]
    else:
        role_utilisateur = None

    if projet is None:
        flash('Projet introuvable.', 'error')
        return redirect(url_for('main.accueil'))
    
    return render_template('main/projet_detaille.html', projet=projet, membres_id=membres_id, membres=membres, role_utilisateur=role_utilisateur, taches = taches)


@bp.route('/projets/<string:id_projet>/ajouter/membre', methods=['GET', 'POST'])
def ajouter_membre(id_projet):
    projet = Projet.query.get(id_projet)
    membres = ProjetMembre.query.filter_by(projet_id=projet.id).all()

    # Vérifier si l'utilisateur actuel est admin du projet
    admin = ProjetMembre.query.filter_by(
        projet_id=id_projet, 
        utilisateur_id=current_user.id, 
        role='Administrateur'
    ).first()

    # L'utilisateur n'est pas membre du projet
    if not admin:
        flash('Vous n\'avez pas les droits pour ajouter un membre à ce projet.', 'error')
        return redirect(url_for('main.projet_detaille', id_projet=id_projet))
    
    utilisateurs_totaux = Utilisateur.query.all()
    utilisateurs_hors_projet = [u for u in utilisateurs_totaux if u.id not in [m.utilisateur_id for m in membres]]
    
    if request.method == 'POST':
        
        try :
            utilisateur_id = request.form.get('user_id')
            role = request.form.get('role')
            id_projet_membre = f"projet_membre_{len(ProjetMembre.query.all()) +1}"

            new_projet_membre = ProjetMembre(id_projet_membre=id_projet_membre, projet_id=id_projet, utilisateur_id=utilisateur_id, role=role)
            db.session.add(new_projet_membre)

            db.session.commit()
            flash('Membre ajouté avec succès !', 'success')

            return redirect(url_for('main.projet_detaille', id_projet=id_projet))
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de l'ajout du membre: {e}")
            flash('Une erreur est survenue lors de l\'ajout du membre.', 'error')

    return render_template('main/ajouter_membre.html', projet=projet, membres=membres, utilisateurs = utilisateurs_hors_projet)

@bp.route('/projets/<string:id_projet>/supprimer/membres/<string:id_membre>', methods=['POST'])
@login_required
def supprimer_membre(id_projet, id_membre):
    projet = Projet.query.get(id_projet)
    if not projet:
        flash('Projet introuvable.', 'error')
        return redirect(url_for('main.accueil'))
    
    # Vérifier si l'utilisateur actuel est admin du projet
    membre_admin = ProjetMembre.query.filter_by(
        projet_id=id_projet, 
        utilisateur_id=current_user.id, 
        role='Administrateur'
    ).first()
    
    if not membre_admin:
        flash('Vous n\'avez pas les droits pour supprimer un membre.', 'error')
        return redirect(url_for('main.projet_detaille', id_projet=id_projet))
    
    # Supprimer le membre
    membre_a_supprimer = ProjetMembre.query.get(id_membre)
    if membre_a_supprimer:
        db.session.delete(membre_a_supprimer)
        db.session.commit()
        flash('Membre supprimé avec succès.', 'success')
    else:
        db.session.rollback()
        flash('Membre introuvable.', 'error')
    
    return redirect(url_for('main.projet_detaille', id_projet=id_projet))

@bp.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():

    if request.method == 'POST' :
        #Récupération des données
        a_propos = request.form.get('a_propos')

        preferences_notif = request.form.get('preferences_notif')

        ancien_mdp = request.form.get('ancien_mdp')
        nouveau_mdp = request.form.get('nouveau_mdp')

        try:
            if(len(ancien_mdp) != 0) :
                if(len(nouveau_mdp) != 0) :
                    # vérification d'avoir des entrées non nulles
                    if(current_user.check_password(ancien_mdp)) :
                        #vérification de l'ancien mdp
                        current_user.set_password(nouveau_mdp)
                        flash('Mot de passe mis à jour avec succès.', 'success')
                    else :
                        flash('Ancien mot de passe incorrect.', 'error')
                        return render_template('main/profil.html')
                flash('Nouveau mot de passe vide.', 'error')
                return render_template('main/profil.html')

            current_user.a_propos = a_propos
            current_user.preferences_notif = preferences_notif
            db.session.commit()
            flash('Profil mis à jour.', 'success')
        except Exception as e :
            db.session.rollback()
            flash('Erreur lors de la modification du profil', 'error')
        


    return render_template('main/profil.html')

@bp.route('/projets/<string:id_projet>/ajouter/tache', methods=['GET', 'POST'])
@login_required
def ajouter_tache(id_projet) :
    membres = ProjetMembre.query.filter_by(projet_id=id_projet).all()

    if request.method == 'POST' :

        id_tache = f"{id_projet}t{ len(Tache.query.all()) + 1}"
        titre = request.form.get('titre')
        description = request.form.get('description')
        date_echeance = datetime.strptime(request.form.get('date_echeance'), '%Y-%m-%d')
        priorite = request.form.get('priorite')

        responsable_tache = request.form.get('respo_id') # peut etre None
        new_tache = Tache(
                id = id_tache,
                titre = titre,
                description = description,
                date_echeance = date_echeance,
                priorite = priorite,
                projet_id = id_projet,
                responsable_id = responsable_tache
            )
        try:          
            db.session.add(new_tache)
            db.session.commit()
            flash('Tache créee avec succès.', 'sucess')
            return redirect(url_for('main.projet_detaille', id_projet = id_projet))
        except Exception as e :
            db.session.rollback()
            flash('Erreur lors de la création de la tache.', 'error')
            return redirect(url_for('main.ajouter_tache', id_projet = id_projet))
        
    return render_template('main/ajouter_tache.html', membres = membres)

@bp.route('/projets/<string:id_projet>/modifier/tache/<string:id_tache>', methods=['POST'])
@login_required
def modifier_tache(id_projet, id_tache):
    #uniquement pour modifier le statut d'une tache
    tache = Tache.query.get(id_tache)
    if not tache:
        flash('Tâche introuvable.', 'error')
        return redirect(url_for('main.projet_detaille', id_projet=id_projet))
    
    nouveau_statut = request.form.get('statut')
    if nouveau_statut not in ['A faire', 'En cours', 'Terminé']:
        flash('Statut invalide.', 'error')
        return redirect(url_for('main.projet_detaille', id_projet=id_projet))
    
    try:
        tache.statut = nouveau_statut
        db.session.commit()
        flash('Statut de la tâche mis à jour.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la modification de la tâche.', 'error')
    
    return redirect(url_for('main.projet_detaille', id_projet=id_projet))

@bp.route('/projets/<string:id_projet>/supprimer/tache/<string:id_tache>', methods=['POST'])
@login_required
def supprimer_tache(id_projet, id_tache):
    tache = Tache.query.get(id_tache)
    if not tache:
        flash('Tâche introuvable.', 'error')
        return redirect(url_for('main.projet_detaille', id_projet=id_projet))
    
    # Vérifier si l'utilisateur actuel est admin du projet
    membre = ProjetMembre.query.filter_by(
        projet_id=id_projet, 
        utilisateur_id=current_user.id, 
        role='Administrateur'
    ).first()
    
    if not membre :
        flash('Vous n\'avez pas les droits pour supprimer une tâche.', 'error')
        return redirect(url_for('main.projet_detaille', id_projet=id_projet))
    
    try:
        db.session.delete(tache)
        db.session.commit()
        flash('Tâche supprimée avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la suppression de la tâche.', 'error')
    
    return redirect(url_for('main.projet_detaille', id_projet=id_projet))

@bp.route('/projets/<string:id_projet>/modifier/tache/<string:id_tache>/responsable/<string:utilisateur_id>', methods=['POST'])
@login_required
def modifier_responsable_tache(id_projet, id_tache, utilisateur_id):
    # Vérifier si la tâche existe
    tache = Tache.query.get(id_tache)
    if not tache:
        flash('Tâche introuvable.', 'error')
        return redirect(url_for('main.projet_detaille', id_projet=id_projet))
    
    # Vérifier si l'utilisateur actuel est membre du projet
    membre = ProjetMembre.query.filter_by(
        projet_id=id_projet, 
        utilisateur_id= utilisateur_id
    ).first()

    role_utilisateur = ProjetMembre.query.filter_by(
        utilisateur_id = current_user.id,
        projet_id = id_projet
    )
    
    # Le contributeur peut déleguer la tache
    if not membre or role_utilisateur.role not in ['Administrateur', 'Contributeur']:
        flash('Impossible de modifier cette tâche.', 'error')
        return redirect(url_for('main.projet_detaille', id_projet=id_projet))
    
    # Récupérer le nouveau responsable depuis le formulaire
    nouveau_responsable_id = request.form.get('responsable_id')
    
    try:
        if nouveau_responsable_id :
            tache.responsable_id = nouveau_responsable_id
            db.session.commit()
            flash('Responsable de la tâche mis à jour.', 'success')
        else :
            flash('Erreur lors de la modification du responsable.', 'error')

    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la modification du responsable.', 'error')
    
    return redirect(url_for('main.projet_detaille', id_projet=id_projet))
