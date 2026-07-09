import csv
import os
from celery_app import celery
from datetime import datetime
from extensions import db
from models.system import ExportJob
from models.application import Application
from models.student import StudentProfile
from services.notification_service import send_google_chat


@celery.task(name='tasks.export.export_applications_csv')
def export_applications_csv(export_job_id):
    export_job = ExportJob.query.get(export_job_id)
    if not export_job:
        return "ExportJob not found"

    export_job.status = 'running'
    db.session.commit()

    try:
        export_dir = os.path.join(
            os.path.dirname(__file__), '..', 'static', 'exports'
        )
        os.makedirs(export_dir, exist_ok=True)

        filename = f"{export_job_id}.csv"
        filepath = os.path.join(export_dir, filename)

        applications = Application.query.filter_by(
            student_id=StudentProfile.query.filter_by(
                user_id=export_job.user_id
            ).first().id
        ).all()

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'Student ID', 'Company Name', 'Drive Title',
                'Application Status', 'Applied At'
            ])
            for app in applications:
                writer.writerow([
                    app.student_id,
                    app.drive.company.name,
                    app.drive.job_title,
                    app.status,
                    app.applied_at.strftime('%Y-%m-%d')
                ])

        export_job.status = 'completed'
        export_job.file_path = f"static/exports/{filename}"
        export_job.completed_at = datetime.utcnow()
        db.session.commit()

        send_google_chat(f"CSV export ready: export job #{export_job_id} completed.")
        return f"Export completed: {filename}"

    except Exception as e:
        export_job.status = 'failed'
        db.session.commit()
        raise e