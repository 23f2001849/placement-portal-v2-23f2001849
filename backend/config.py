import os
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(BASE_DIR, '.env'))

# Flask core
SECRET_KEY = os.environ.get('SECRET_KEY') or 'ppa-v2-dev-secret-change-in-prod'

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'placement.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Debug
DEBUG = True

# JWT
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'ppa-v2-jwt-secret-change-in-prod'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

# Google Chat
GOOGLE_CHAT_WEBHOOK_URL = os.environ.get('GOOGLE_CHAT_WEBHOOK_URL', '')

# Flask-Mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME', '')