import os
from flask import Flask, send_from_directory
from extensions import db, jwt, mail
import models
from models import User, CompanyProfile, StudentProfile, PlacementDrive, Application, Placement, NotificationLog, ExportJob
from config import(
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    DEBUG,
    JWT_SECRET_KEY,
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_REFRESH_TOKEN_EXPIRES,
    MAIL_SERVER,
    MAIL_PORT,
    MAIL_USE_TLS,
    MAIL_USERNAME,
    MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER
)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    import yaml
    from flasgger import Swagger
    yaml_path = os.path.join(app.root_path, 'api.yaml')
    with open(yaml_path, 'r') as f:
        template = yaml.safe_load(f)
    Swagger(app, template=template)

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from routes.admin import admin_bp
    app.register_blueprint(admin_bp)
    from routes.company import company_bp
    app.register_blueprint(company_bp)
    from routes.student import student_bp
    app.register_blueprint(student_bp)
    from routes.exports import exports_bp
    app.register_blueprint(exports_bp)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_vue(path):
        dist_dir = os.path.join(app.root_path, 'static', 'dist')
        if path and os.path.exists(os.path.join(dist_dir, path)):
            return send_from_directory(dist_dir, path)
        return send_from_directory(dist_dir, 'index.html')

    with app.app_context():
        os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
        db.create_all()
        seed_admin()

    return app


def seed_admin():
    from models.user import User
    from werkzeug.security import generate_password_hash
    admin = User.query.filter_by(role='admin').first()
    if not admin:
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
from celery_app import make_celery
celery = make_celery(app)

if __name__ == '__main__':
    app.run(debug=DEBUG, port=5000)