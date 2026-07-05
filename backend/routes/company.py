from flask import Blueprint, request, jsonify, g
from extensions import db
from models.user import User
from datetime import date
from models.company import CompanyProfile
from models.drive import PlacementDrive
from models.application import Application
from models.placement import Placement
from utils.decorators import approved_company_required
from flask_jwt_extended import get_jwt_identity

company_bp = Blueprint('company', __name__)


def get_company_profile():
    user_id = get_jwt_identity()
    return CompanyProfile.query.filter_by(user_id=int(user_id)).first()


@company_bp.route('/api/company/dashboard', methods=['GET'])
@approved_company_required
def dashboard():
    company = get_company_profile()

    drives = company.drives.all()
    drive_data = []
    for drive in drives:
        drive_data.append({
            'id': drive.id,
            'job_title': drive.job_title,
            'status': drive.status,
            'applicant_count': drive.applications.count()
        })

    return jsonify({
        'company_name': company.name,
        'approval_status': company.approval_status,
        'total_drives': len(drives),
        'drives': drive_data
    }), 200


@company_bp.route('/api/company/profile', methods=['GET'])
@approved_company_required
def get_profile():
    company = get_company_profile()

    return jsonify({
        'id': company.id,
        'name': company.name,
        'industry': company.industry,
        'website': company.website,
        'hr_contact': company.hr_contact,
        'description': company.description,
        'approval_status': company.approval_status
    }), 200


@company_bp.route('/api/company/profile', methods=['PUT'])
@approved_company_required
def update_profile():
    company = get_company_profile()
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    allowed_fields = ['name', 'industry', 'website', 'hr_contact', 'description']
    for field in allowed_fields:
        if field in data:
            setattr(company, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200


@company_bp.route('/api/company/drives', methods=['POST'])
@approved_company_required
def create_drive():
    company = get_company_profile()
    data = request.get_json()

    if not data or not data.get('job_title'):
        return jsonify({'message': 'job_title is required'}), 400

    from datetime import date
    deadline = None
    if data.get('application_deadline'):
        try:
            deadline = date.fromisoformat(data['application_deadline'])
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    drive = PlacementDrive(
        company_id=company.id,
        job_title=data['job_title'],
        job_description=data.get('job_description'),
        min_cgpa=data.get('min_cgpa'),
        allowed_departments=data.get('allowed_departments'),
        salary_range=data.get('salary_range'),
        location=data.get('location'),
        application_deadline=deadline,
        status='pending'
    )
    db.session.add(drive)
    db.session.commit()

    return jsonify({'message': 'Drive created successfully', 'drive_id': drive.id}), 201


@company_bp.route('/api/company/drives', methods=['GET'])
@approved_company_required
def list_drives():
    company = get_company_profile()
    drives = company.drives.all()

    return jsonify([{
        'id': d.id,
        'job_title': d.job_title,
        'status': d.status,
        'min_cgpa': d.min_cgpa,
        'allowed_departments': d.allowed_departments,
        'salary_range': d.salary_range,
        'location': d.location,
        'application_deadline': d.application_deadline.isoformat() if d.application_deadline else None,
        'applicant_count': d.applications.count(),
        'created_at': d.created_at.isoformat()
    } for d in drives]), 200


@company_bp.route('/api/company/drives/<int:drive_id>', methods=['PUT'])
@approved_company_required
def edit_drive(drive_id):
    company = get_company_profile()
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first()

    if not drive:
        return jsonify({'message': 'Drive not found'}), 404

    if drive.status != 'pending':
        return jsonify({'message': 'Only pending drives can be edited'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    editable_fields = ['job_title', 'job_description', 'min_cgpa',
                       'allowed_departments', 'salary_range', 'location',
                       'application_deadline']
    for field in editable_fields:
        if field in data:
            setattr(drive, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Drive updated successfully'}), 200


@company_bp.route('/api/company/drives/<int:drive_id>/close', methods=['PUT'])
@approved_company_required
def close_drive(drive_id):
    company = get_company_profile()
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first()

    if not drive:
        return jsonify({'message': 'Drive not found'}), 404

    if drive.status not in ['pending', 'approved']:
        return jsonify({'message': 'Drive cannot be closed'}), 400

    drive.status = 'closed'
    db.session.commit()
    return jsonify({'message': 'Drive closed'}), 200


@company_bp.route('/api/company/drives/<int:drive_id>/applications', methods=['GET'])
@approved_company_required
def drive_applications(drive_id):
    company = get_company_profile()
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first()

    if not drive:
        return jsonify({'message': 'Drive not found'}), 404

    applications = drive.applications.all()

    return jsonify([{
        'id': a.id,
        'student_name': a.student.name,
        'student_id': a.student_id,
        'roll_number': a.student.roll_number,
        'department': a.student.department,
        'cgpa': a.student.cgpa,
        'status': a.status,
        'remark': a.remark,
        'applied_at': a.applied_at.isoformat()
    } for a in applications]), 200


@company_bp.route('/api/company/applications/<int:application_id>/status', methods=['PUT'])
@approved_company_required
def update_application_status(application_id):
    company = get_company_profile()
    application = Application.query.get(application_id)

    if not application:
        return jsonify({'message': 'Application not found'}), 404

    if application.drive.company_id != company.id:
        return jsonify({'message': 'Access denied'}), 403

    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'message': 'status is required'}), 400

    new_status = data['status']

    valid_transitions = {
        'applied': ['shortlisted', 'rejected'],
        'shortlisted': ['selected', 'rejected'],
    }

    current_status = application.status
    if current_status not in valid_transitions:
        return jsonify({'message': 'No further transitions allowed'}), 400

    if new_status not in valid_transitions[current_status]:
        return jsonify({
            'message': f'Invalid transition: {current_status} → {new_status}'
        }), 400

    application.status = new_status
    if 'remark' in data:
        application.remark = data['remark']

    if new_status == 'selected':
        existing = Placement.query.filter_by(application_id=application.id).first()
        if not existing:
            placement = Placement(
                student_id=application.student_id,
                drive_id=application.drive_id,
                application_id=application.id
            )
            db.session.add(placement)

    db.session.commit()
    return jsonify({'message': f'Application status updated to {new_status}'}), 200