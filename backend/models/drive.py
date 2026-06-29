from extensions import db
from datetime import datetime

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profiles.id'), nullable=False, index=True)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text)
    min_cgpa = db.Column(db.Float)
    allowed_departments = db.Column(db.String(200)) 
    salary_range = db.Column(db.String(100))
    location = db.Column(db.String(100))
    application_deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship('CompanyProfile', backref=db.backref('drives', lazy='dynamic'))

    def __repr__(self):
        return f'<PlacementDrive {self.job_title} at {self.status}>'
    
    