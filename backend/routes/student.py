from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.student import StudentProfile
from models.drive import PlacementDrive
from models.application import Application
from models.placement import Placement
from utils.decorators import role_required
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import IntegrityError
import os

student_bp = Blueprint('student', __name__)


def get_student_profile():
    user_id = get_jwt_identity()
    return StudentProfile.query.filter_by(user_id=int(user_id)).first()


@student_bp.route('/api/student/dashboard', methods=['GET'])
@role_required('student')
def dashboard():
    student = get_student_profile()

    approved_drives = PlacementDrive.query.filter_by(status='approved').count()
    my_applications = Application.query.filter_by(student_id=student.id).count()
    my_placements = Placement.query.filter_by(student_id=student.id).count()

    return jsonify({
        'student_name': student.name,
        'approved_drives': approved_drives,
        'my_applications': my_applications,
        'my_placements': my_placements
    }), 200


@student_bp.route('/api/student/profile', methods=['GET'])
@role_required('student')
def get_profile():
    student = get_student_profile()

    return jsonify({
        'id': student.id,
        'name': student.name,
        'roll_number': student.roll_number,
        'department': student.department,
        'phone': student.phone,
        'cgpa': student.cgpa,
        'year_of_study': student.year_of_study,
        'skills': student.skills,
        'education': student.education,
        'resume_path': student.resume_path
    }), 200


@student_bp.route('/api/student/profile', methods=['PUT'])
@role_required('student')
def update_profile():
    student = get_student_profile()
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    allowed_fields = ['name', 'roll_number', 'department', 'phone',
                      'cgpa', 'year_of_study', 'skills', 'education']
    for field in allowed_fields:
        if field in data:
            setattr(student, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200


@student_bp.route('/api/drives', methods=['GET'])
@role_required('student')
def list_drives():
    q = request.args.get('q', '').strip()
    department = request.args.get('department', '').strip()
    min_cgpa = request.args.get('min_cgpa', type=float)

    query = PlacementDrive.query.filter_by(status='approved')

    if q:
        query = query.filter(
            db.or_(
                PlacementDrive.job_title.ilike(f'%{q}%'),
                PlacementDrive.location.ilike(f'%{q}%')
            )
        )

    if department:
        query = query.filter(
            PlacementDrive.allowed_departments.ilike(f'%{department}%')
        )

    if min_cgpa is not None:
        query = query.filter(
            db.or_(
                PlacementDrive.min_cgpa == None,
                PlacementDrive.min_cgpa <= min_cgpa
            )
        )

    drives = query.all()

    return jsonify([{
        'id': d.id,
        'job_title': d.job_title,
        'company_name': d.company.name,
        'location': d.location,
        'salary_range': d.salary_range,
        'min_cgpa': d.min_cgpa,
        'allowed_departments': d.allowed_departments,
        'application_deadline': d.application_deadline.isoformat() if d.application_deadline else None,
        'applicant_count': d.applications.count()
    } for d in drives]), 200


@student_bp.route('/api/drives/<int:drive_id>', methods=['GET'])
@role_required('student')
def drive_detail(drive_id):
    drive = PlacementDrive.query.filter_by(id=drive_id, status='approved').first()

    if not drive:
        return jsonify({'message': 'Drive not found'}), 404

    return jsonify({
        'id': drive.id,
        'job_title': drive.job_title,
        'job_description': drive.job_description,
        'company_name': drive.company.name,
        'location': drive.location,
        'salary_range': drive.salary_range,
        'min_cgpa': drive.min_cgpa,
        'allowed_departments': drive.allowed_departments,
        'application_deadline': drive.application_deadline.isoformat() if drive.application_deadline else None,
    }), 200


@student_bp.route('/api/student/applications', methods=['POST'])
@role_required('student')
def apply():
    student = get_student_profile()
    data = request.get_json()

    if not data or 'drive_id' not in data:
        return jsonify({'message': 'drive_id is required'}), 400

    drive = PlacementDrive.query.filter_by(
        id=data['drive_id'], status='approved'
    ).first()

    if not drive:
        return jsonify({'message': 'Drive not found or not open'}), 404

    if drive.min_cgpa is not None:
        if student.cgpa is None:
            return jsonify({'message': 'CGPA not set on your profile'}), 422
        if student.cgpa < drive.min_cgpa:
            return jsonify({'message': f'Minimum CGPA required: {drive.min_cgpa}'}), 422

    if drive.allowed_departments:
        if student.department is None:
            return jsonify({'message': 'Department not set on your profile'}), 422
        allowed = [d.strip() for d in drive.allowed_departments.split(',')]
        if student.department not in allowed:
            return jsonify({'message': 'Your department is not eligible'}), 422

    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()
    if existing:
        return jsonify({'message': 'Already applied to this drive'}), 409

    try:
        application = Application(
            student_id=student.id,
            drive_id=drive.id,
            status='applied'
        )
        db.session.add(application)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Already applied to this drive'}), 409

    return jsonify({'message': 'Application submitted successfully'}), 201


@student_bp.route('/api/student/applications', methods=['GET'])
@role_required('student')
def application_history():
    student = get_student_profile()
    applications = Application.query.filter_by(student_id=student.id).all()

    return jsonify([{
        'id': a.id,
        'drive_title': a.drive.job_title,
        'company_name': a.drive.company.name,
        'status': a.status,
        'remark': a.remark,
        'applied_at': a.applied_at.isoformat(),
        'updated_at': a.updated_at.isoformat()
    } for a in applications]), 200


@student_bp.route('/api/student/profile/resume', methods=['POST'])
@role_required('student')
def upload_resume():
    student = get_student_profile()

    if 'resume' not in request.files:
        return jsonify({'message': 'No file uploaded'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'message': 'Only PDF files allowed'}), 400

    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    if size > 2 * 1024 * 1024:
        return jsonify({'message': 'File too large. Max 2MB'}), 400

    upload_dir = os.path.join(
        os.path.dirname(__file__), '..', 'static', 'uploads', 'resumes'
    )
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{student.user_id}_{file.filename}"
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    student.resume_path = f"uploads/resumes/{filename}"
    db.session.commit()

    return jsonify({
        'message': 'Resume uploaded successfully',
        'resume_path': student.resume_path
    }), 200