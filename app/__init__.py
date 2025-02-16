from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.routes import auth, main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    # Importer les modèles ici pour éviter les imports circulaires
    from app.models.utilisateur import Utilisateur  # Changé de User à Utilisateur

    @login_manager.user_loader
    def load_user(user_id):
        return Utilisateur.query.get(user_id)  # Changé de User à Utilisateur

    return app
