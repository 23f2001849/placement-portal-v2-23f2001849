from extensions import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id'), nullable = False, index=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable=False, index=True)
    status = db.Column(db.String(20), default='applied')
    remark = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='uq_student_drive'),
    )

    student = db.relationship('StudentProfile', backref = db.backref('applications', lazy='dynamic'))
    drive = db.relationship('PlacementDrive', backref = db.backref('applications', lazy='dynamic'))

    def __repr__(self):
        return f'<Application Student ID: {self.student_id}, Drive ID: {self.drive_id}, Status: {self.status}>'
    
    