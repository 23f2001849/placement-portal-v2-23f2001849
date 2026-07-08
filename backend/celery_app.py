from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker='redis://localhost:6379/1',
        backend='redis://localhost:6379/2'
    )

    celery.conf.update(
        timezone='Asia/Kolkata',
        beat_schedule={
            'daily-reminder': {
                'task': 'tasks.reminder.send_daily_reminder',
                'schedule': crontab(hour=8, minute=0),
            },
            'monthly-report': {
                'task': 'tasks.report.generate_monthly_report',
                'schedule': crontab(day_of_month=1, hour=6, minute=0),
            },
        }
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery