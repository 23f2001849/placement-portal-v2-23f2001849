from flask import Blueprint, jsonify, send_from_directory
from extensions import db
from models.system import ExportJob
from utils.decorators import role_required
from flask_jwt_extended import get_jwt_identity
from tasks.export import export_applications_csv
import os

exports_bp = Blueprint('exports', __name__)


@exports_bp.route('/api/exports/applications', methods=['POST'])
@role_required('student', 'company', 'admin')
def trigger_export():
    user_id = int(get_jwt_identity())

    export_job = ExportJob(
        user_id=user_id,
        status='pending'
    )
    db.session.add(export_job)
    db.session.commit()

    task = export_applications_csv.delay(export_job.id)
    export_job.task_id = task.id
    db.session.commit()

    return jsonify({
        'export_id': export_job.id,
        'task_id': task.id,
        'message': 'Export started'
    }), 202


@exports_bp.route('/api/exports/<int:export_id>', methods=['GET'])
@role_required('student', 'company', 'admin')
def get_export_status(export_id):
    user_id = int(get_jwt_identity())
    export_job = ExportJob.query.filter_by(
        id=export_id, user_id=user_id
    ).first()

    if not export_job:
        return jsonify({'message': 'Export job not found'}), 404

    response = {
        'export_id': export_job.id,
        'status': export_job.status,
        'file_url': None
    }

    if export_job.status == 'completed' and export_job.file_path:
        response['file_url'] = f"/api/exports/{export_id}/download"

    return jsonify(response), 200


@exports_bp.route('/api/exports/<int:export_id>/download', methods=['GET'])
@role_required('student', 'company', 'admin')
def download_export(export_id):
    user_id = int(get_jwt_identity())
    export_job = ExportJob.query.filter_by(
        id=export_id, user_id=user_id
    ).first()

    if not export_job or export_job.status != 'completed':
        return jsonify({'message': 'File not ready'}), 404

    export_dir = os.path.join(
        os.path.dirname(__file__), '..', 'static', 'exports'
    )
    filename = f"{export_id}.csv"
    return send_from_directory(export_dir, filename, as_attachment=True)