from extensions import db
from datetime import datetime



class CompanyProfile(db.Model):
    __tablename__ = 'company_profiles'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable = False)
    name = db.Column(db.String(120), nullable = False, index=True)
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(200))
    industry = db.Column(db.String(100), index=True)
    description = db.Column(db.Text)
    approval_status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('company_profile', uselist=False))

    def __repr__(self):
        return f'<CompanyProfile {self.name}>'
    
