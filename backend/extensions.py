from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import redis

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
redis_client = redis.Redis(host='localhost', port=6379, db=3, decode_responses=True)