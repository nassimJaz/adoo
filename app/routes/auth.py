from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

from app.models.utilisateur import Utilisateur
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirection vers la page de connexion (pour flask login qui prend directement la route login)
    return redirect(url_for('auth.connexion'))

@bp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('main.accueil'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        mdp = request.form.get('password')

        user = Utilisateur.query.filter_by(email=email).first()

        if user and user.check_password(mdp) :
            login_user(user)
            flash('Connexion réussie !', 'success')
            return redirect(url_for('main.accueil'))
        else:
            flash('Email ou mot de passe incorrect.', 'error')

    return render_template('auth/connexion.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.connexion')) # retour à la connexion

@bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        mdp = request.form.get('mdp')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
    
        nb_users = Utilisateur.query.count()
        user_id = f"user_{nb_users + 1}"

        # On vérifie que l'utilisateur est unique, retourne un user ou None
        user = Utilisateur.query.filter_by(email=email).first()

        if user:
            flash('Cet email est déjà utilisé.', 'error')
            return redirect(url_for('auth.inscription')) # réinscription
    
        new_user = Utilisateur(id=user_id, email=email, nom=nom, prenom=prenom)
        new_user.set_password(mdp) # mdp hashé

        try:
            db.session.add(new_user)
            db.session.commit() #inscription du user dans la bdd
            flash('Inscription réussie !', 'success')
            return redirect(url_for('auth.connexion'))
        
        except Exception as e:
            db.session.rollback() #retour à l'état initial si modification de la bdd
            flash('Une erreur est survenue lors de l\'inscription.', 'error')
            return redirect(url_for('auth.inscription'))

    return render_template('auth/inscription.html')
