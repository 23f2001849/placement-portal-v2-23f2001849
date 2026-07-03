from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from models.company import CompanyProfile


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') not in roles:
                return jsonify({'message': 'Access denied'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def approved_company_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') != 'company':
            return jsonify({'message': 'Access denied'}), 403
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()
        profile = CompanyProfile.query.filter_by(user_id=int(user_id)).first()
        if not profile or profile.approval_status != 'approved':
            return jsonify({'message': 'Company not approved'}), 403
        return fn(*args, **kwargs)
    return wrapper