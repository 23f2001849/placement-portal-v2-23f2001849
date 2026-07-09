from celery_app import celery
from datetime import date
from dateutil.relativedelta import relativedelta
from extensions import db, mail
from flask_mail import Message
from models.drive import PlacementDrive
from models.application import Application
from models.placement import Placement
from models.user import User
from flask import render_template


@celery.task(name='tasks.report.generate_monthly_report')
def generate_monthly_report():
    today = date.today()
    first_of_month = today.replace(day=1)
    last_month_start = first_of_month - relativedelta(months=1)
    last_month_end = first_of_month

    drives_created = PlacementDrive.query.filter(
        PlacementDrive.created_at >= last_month_start,
        PlacementDrive.created_at < last_month_end
    ).count()

    applications_received = Application.query.filter(
        Application.applied_at >= last_month_start,
        Application.applied_at < last_month_end
    ).count()

    students_selected = Placement.query.filter(
        Placement.placed_at >= last_month_start,
        Placement.placed_at < last_month_end
    ).count()

    admin = User.query.filter_by(role='admin').first()
    if not admin:
        return "No admin found"

    body = f"""
    Monthly Placement Report - {last_month_start.strftime('%B %Y')}

    Drives Created: {drives_created}
    Applications Received: {applications_received}
    Students Selected: {students_selected}

    Generated on {today}
    """

    msg = Message(
        subject=f"Monthly Placement Report - {last_month_start.strftime('%B %Y')}",
        recipients=[admin.email],
        body=body
    )
    mail.send(msg)

    return f"Monthly report sent to {admin.email}"