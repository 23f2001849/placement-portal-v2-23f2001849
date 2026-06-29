from extensions import db
from datetime import datetime

class Placement(db.Model):
    __tablename__ = 'placements'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id'), nullable=False, index=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable = False, index= True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), unique= True, nullable = False)
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('StudentProfile', backref = db.backref('placement', uselist = False))
    drive = db.relationship('PlacementDrive', backref = db.backref('placements', lazy='dynamic'))
    application = db.relationship('Application', backref = db.backref('placement', uselist = False))

    def __repr__(self):
        return f'<Placement student={self.student_id} drive={self.drive_id}>'
    
