import os

class Config:
    SECRET_KEY = os.environ.get('E_VRIFICATION_SECRET_KEY')
    MAIL_SERVER = os.environ.get('EMAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('EMAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('EMAIL_ENCY_TLS') == 'True'
    MAIL_USE_SSL = os.environ.get('EMAIL_ENCY_SSL') == 'True'
    MAIL_USERNAME = os.environ.get('EMAIL_APP_USERNAME')
    MAIL_PASSWORD = os.environ.get('EMAIL_APP_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_APP_USERNAME')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    OAUTHLIB_INSECURE_TRANSPORT = os.getenv('OAUTHLIB_INSECURE_TRANSPORT') or '1'
    OAUTHLIB_RELAX_TOKEN_SCOPE = os.getenv('OAUTHLIB_RELAX_TOKEN_SCOPE') or '1'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
