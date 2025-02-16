from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/accueil')
def index():
    return render_template('main/accueil.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')