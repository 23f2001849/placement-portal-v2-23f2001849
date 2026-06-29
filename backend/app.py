import os
from flask import Flask
from extensions import db, jwt
from config import(
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    DEBUG
)
import models

def create_app():
    app = Flask(__name__)

    # Load config into app
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    # Connect extensions to app
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok = True)
        db.create_all
        seed_admin()

    return app

from models import User, CompanyProfile, StudentProfile, PlacementDrive, Application, Placement, NotificationLog, ExportJob

def seed_admin():
    from models.user import User
    from werkzeug.security import generate_password_hash

    # Check if admin user already exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        # Create a new admin user
        admin = User(
            email='admin@gmail.com',
            password=generate_password_hash('admin'),  
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")

    else:
        print("Admin user already exists.")

app = create_app()

if __name__ == '__main__':
    app.run(debug=DEBUG, port=5000)