from extensions import db
from datetime import datetime


class NotificationLog(db.Model):
    __tablename__ = 'notification_logs'

    id = db.Column(db.Integer, primary_key=True)
    notification_type = db.Column(db.String(50), nullable=False)
    recipient = db.Column(db.String(150))
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='sent')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<NotificationLog {self.notification_type} to {self.recipient}>'


class ExportJob(db.Model):
    __tablename__ = 'export_jobs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    task_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='pending')
    file_path = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('export_jobs', lazy='dynamic'))

    def __repr__(self):
        return f'<ExportJob {self.task_id} ({self.status})>'