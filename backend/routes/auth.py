from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from extensions import db
from models.user import User
from models.student import StudentProfile
from models.company import CompanyProfile

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/register/student', methods=['POST'])
def register_student():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    required = ['email', 'password', 'name']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({'message': f'{field} is required'}), 400

    if data['email'] == '' or '@' not in data['email']:
        return jsonify({'message': 'Invalid email'}), 400

    existing = User.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'message': 'Email already registered'}), 409

    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role='student'
    )
    db.session.add(user)
    db.session.flush()

    profile = StudentProfile(
        user_id=user.id,
        name=data['name']
    )
    db.session.add(profile)
    db.session.commit()

    return jsonify({'message': 'Student registered successfully'}), 201


@auth_bp.route('/api/register/company', methods=['POST'])
def register_company():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    required = ['email', 'password', 'name']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({'message': f'{field} is required'}), 400

    existing = User.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'message': 'Email already registered'}), 409

    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role='company'
    )
    db.session.add(user)
    db.session.flush()

    profile = CompanyProfile(
        user_id=user.id,
        name=data['name']
    )
    db.session.add(profile)
    db.session.commit()

    return jsonify({'message': 'Company registered. Awaiting admin approval.'}), 201


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password required'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    if user.is_blacklisted:
        return jsonify({'message': 'Account has been suspended'}), 403

    if user.role == 'company':
        profile = CompanyProfile.query.filter_by(user_id=user.id).first()
        if not profile or profile.approval_status != 'approved':
            return jsonify({'message': 'Company account pending admin approval'}), 403

    additional_claims = {'role': user.role}
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims=additional_claims
    )

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'role': user.role,
        'email': user.email
    }), 200

@auth_bp.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({'message': 'User not found'}), 404

    additional_claims = {'role': user.role}
    new_access_token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims
    )

    return jsonify({'access_token': new_access_token}), 200

@auth_bp.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/api/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'email': user.email,
        'role': user.role
    }), 200