from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.company import CompanyProfile
from models.student import StudentProfile
from models.drive import PlacementDrive
from models.application import Application
from models.placement import Placement
from utils.decorators import role_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/api/admin/dashboard', methods=['GET'])
@role_required('admin')
def dashboard():
    total_students = StudentProfile.query.count()
    total_companies = CompanyProfile.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()
    total_placements = Placement.query.count()

    return jsonify({
        'total_students': total_students,
        'total_companies': total_companies,
        'total_drives': total_drives,
        'total_applications': total_applications,
        'total_placements': total_placements
    }), 200


@admin_bp.route('/api/admin/companies', methods=['GET'])
@role_required('admin')
def list_companies():
    status = request.args.get('status')
    query = CompanyProfile.query

    if status:
        query = query.filter_by(approval_status=status)

    companies = query.all()

    return jsonify([{
        'id': c.id,
        'name': c.name,
        'industry': c.industry,
        'website': c.website,
        'hr_contact': c.hr_contact,
        'approval_status': c.approval_status,
        'email': c.user.email,
        'is_blacklisted': c.user.is_blacklisted,
        'created_at': c.created_at.isoformat()
    } for c in companies]), 200


@admin_bp.route('/api/admin/companies/<int:company_id>/approve', methods=['PUT'])
@role_required('admin')
def approve_company(company_id):
    company = CompanyProfile.query.get(company_id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    company.approval_status = 'approved'
    db.session.commit()

    return jsonify({'message': 'Company approved'}), 200


@admin_bp.route('/api/admin/companies/<int:company_id>/reject', methods=['PUT'])
@role_required('admin')
def reject_company(company_id):
    company = CompanyProfile.query.get(company_id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    company.approval_status = 'rejected'
    db.session.commit()

    return jsonify({'message': 'Company rejected'}), 200


@admin_bp.route('/api/admin/companies/<int:company_id>/blacklist', methods=['PUT'])
@role_required('admin')
def blacklist_company(company_id):
    company = CompanyProfile.query.get(company_id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    company.user.is_blacklisted = True

    open_drives = company.drives.filter(
        PlacementDrive.status.in_(['pending', 'approved'])
    ).all()
    for drive in open_drives:
        drive.status = 'closed'

    db.session.commit()

    return jsonify({
        'message': 'Company blacklisted and drives closed',
        'drives_closed': len(open_drives)
    }), 200


@admin_bp.route('/api/admin/students', methods=['GET'])
@role_required('admin')
def list_students():
    q = request.args.get('q', '').strip()
    query = StudentProfile.query

    if q:
        query = query.join(User).filter(
            db.or_(
                StudentProfile.name.ilike(f'%{q}%'),
                StudentProfile.roll_number.ilike(f'%{q}%'),
                User.email.ilike(f'%{q}%')
            )
        )

    students = query.all()

    return jsonify([{
        'id': s.id,
        'name': s.name,
        'roll_number': s.roll_number,
        'department': s.department,
        'cgpa': s.cgpa,
        'email': s.user.email,
        'is_blacklisted': s.user.is_blacklisted,
        'created_at': s.created_at.isoformat()
    } for s in students]), 200


@admin_bp.route('/api/admin/students/<int:student_id>/blacklist', methods=['PUT'])
@role_required('admin')
def blacklist_student(student_id):
    student = StudentProfile.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    student.user.is_blacklisted = True
    db.session.commit()

    return jsonify({'message': 'Student blacklisted'}), 200


@admin_bp.route('/api/admin/drives', methods=['GET'])
@role_required('admin')
def list_drives():
    status = request.args.get('status')
    query = PlacementDrive.query

    if status:
        query = query.filter_by(status=status)

    drives = query.all()

    return jsonify([{
        'id': d.id,
        'job_title': d.job_title,
        'company_name': d.company.name,
        'company_id': d.company_id,
        'status': d.status,
        'min_cgpa': d.min_cgpa,
        'allowed_departments': d.allowed_departments,
        'application_deadline': d.application_deadline.isoformat() if d.application_deadline else None,
        'created_at': d.created_at.isoformat()
    } for d in drives]), 200


@admin_bp.route('/api/admin/drives/<int:drive_id>/approve', methods=['PUT'])
@role_required('admin')
def approve_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({'message': 'Drive not found'}), 404

    if drive.status != 'pending':
        return jsonify({'message': f'Cannot approve a drive with status {drive.status}'}), 400

    drive.status = 'approved'
    db.session.commit()

    return jsonify({'message': 'Drive approved'}), 200


@admin_bp.route('/api/admin/drives/<int:drive_id>/reject', methods=['PUT'])
@role_required('admin')
def reject_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({'message': 'Drive not found'}), 404

    if drive.status != 'pending':
        return jsonify({'message': f'Cannot reject a drive with status {drive.status}'}), 400

    drive.status = 'rejected'
    db.session.commit()

    return jsonify({'message': 'Drive rejected'}), 200


@admin_bp.route('/api/admin/applications', methods=['GET'])
@role_required('admin')
def list_applications():
    drive_id = request.args.get('drive_id', type=int)
    student_id = request.args.get('student_id', type=int)

    query = Application.query

    if drive_id:
        query = query.filter_by(drive_id=drive_id)
    if student_id:
        query = query.filter_by(student_id=student_id)

    applications = query.all()

    return jsonify([{
        'id': a.id,
        'student_name': a.student.name,
        'student_id': a.student_id,
        'drive_title': a.drive.job_title,
        'company_name': a.drive.company.name,
        'drive_id': a.drive_id,
        'status': a.status,
        'remark': a.remark,
        'applied_at': a.applied_at.isoformat(),
        'updated_at': a.updated_at.isoformat()
    } for a in applications]), 200