import os
from datetime import timedelta

# Absolute path to the backend/ folder itself
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask core secret - used to sign session cookies 
SECRET_KEY = os.environ.get("SECRET_KEY") or 'ppa-v2-dev-secret-change-in-prod'

# SQLAlchemy - SQLite file inside backend/instance/
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'placement.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Development flag
DEBUG = True