from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

bp = Blueprint('auth', __name__)

@bp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    return render_template('auth/connexion.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    return render_template('auth/register.html')