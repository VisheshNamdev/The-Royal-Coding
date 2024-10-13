from flask import Flask,g,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_mail import Mail
from .config import Config
import os
from os import path
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
import logging
from logging.handlers import RotatingFileHandler
from flask_session import Session
import smtplib

mail = Mail()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'helloworld')
    db_uri = os.getenv('DB_URI')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 20,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 1800
    }
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/images')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max file size
    app.config['CKEDITOR_PKG_TYPE'] = 'full'
    app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
    app.config['CKEDITOR_FILE_UPLOADER'] = 'views.upload'
    app.config['SESSION_TYPE'] = 'filesystem'

    Session(app)
    db.init_app(app)
    mail.init_app(app)
    
    oauth = OAuth(app)
    linkedin = oauth.register(
        name='linkedin',
        client_id=os.getenv('LINKEDIN_CLIENT_ID'),
        client_secret=os.getenv('LINKEDIN_CLIENT_SECRET'),
        access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
        authorize_url='https://www.linkedin.com/oauth/v2/authorization',
        client_kwargs={'scope': 'openid profile email'}
    )
    
    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid profile email'}
    )
    
    app.config['oauth'] = oauth
    
    if not app.debug:
        file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
        file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    
    migrate = Migrate(app, db)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    ckeditor = CKEditor(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    from .models import User
    # verify_smtp_connection()
    # with app.app_context():
    #     create_database(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
        
    @app.before_request
    def before_request_func():
        g.user = None
        if 'user_id' in session:
            g.user = User.query.get(session['user_id'])

    @app.teardown_request
    def teardown_request_func(exception=None):
        db.session.remove()    

    
    return app

def create_database(app):
    with app.app_context():
        try:
            db.create_all()
            print("Connected to the MySQL database!")
        except Exception as e:
            print("Failed to connect to the MySQL database.")
            print(e)
            


def verify_smtp_connection():
    try:
        server = smtplib.SMTP(os.environ.get('EMAIL_SERVER'),os.environ.get('EMAIL_PORT'))
        server.starttls()
        server.login(os.environ.get('EMAIL_APP_USERNAME'), os.environ.get('EMAIL_APP_PASSWORD'))  # Replace with your actual email password
        server.quit()
        print('Successfully connected to the SMTP server.')
    except Exception as e:
        print(f'Failed to connect: {e}')


            
            