import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-very-secret'
    
    DB_NAME = "database.db"
    INSTANCE_PATH = os.path.join(basedir, 'instance')
    DB_PATH = os.path.join(INSTANCE_PATH, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        
        os.makedirs(Config.INSTANCE_PATH, exist_ok=True)
