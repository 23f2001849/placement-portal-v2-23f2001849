from celery_app import celery
from datetime import date, timedelta
from extensions import db
from models.application import Application
from models.drive import PlacementDrive
from services.notification_service import notify_and_log


@celery.task(name='tasks.reminder.send_daily_reminder')
def send_daily_reminder():
    today = date.today()
    deadline_soon = today + timedelta(days=2)

    drives = PlacementDrive.query.filter(
        PlacementDrive.status == 'approved',
        PlacementDrive.application_deadline == deadline_soon
    ).all()

    count = 0
    for drive in drives:
        applications = Application.query.filter_by(
            drive_id=drive.id,
            status='applied'
        ).all()

        for application in applications:
            student = application.student
            message = (
                f"Reminder: Your application for *{drive.job_title}* "
                f"at *{drive.company.name}* has a deadline on "
                f"{drive.application_deadline}. Log in to check your status."
            )
            notify_and_log(
                notification_type='daily_reminder',
                recipient=student.user.email,
                message=message
            )
            count += 1

    return f"Sent {count} reminders"