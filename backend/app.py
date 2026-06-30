import os
from flask import Flask, app
from extensions import db, jwt
import models
from models import User, CompanyProfile, StudentProfile, PlacementDrive, Application, Placement, NotificationLog, ExportJob

from config import(
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    DEBUG,
    JWT_SECRET_KEY,
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_REFRESH_TOKEN_EXPIRES
)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES

    db.init_app(app)
    jwt.init_app(app)

    import yaml
    from flasgger import Swagger
    yaml_path = os.path.join(app.root_path, 'api.yaml')
    with open(yaml_path, 'r') as f:
        template = yaml.safe_load(f)
    Swagger(app, template=template)
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    with app.app_context():
        os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
        db.create_all()
        seed_admin()

    return app

def seed_admin():
    from models.user import User
    from werkzeug.security import generate_password_hash

    # Check if admin user already exists
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        # Create a new admin user
        admin = User(
            email='admin@gmail.com',
            password_hash=generate_password_hash('admin'),  
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