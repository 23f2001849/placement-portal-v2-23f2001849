from extensions import db
from datetime import datetime

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique= True, nullable = False)
    name = db.Column(db.String(120), nullable = False, index=True)
    roll_number = db.Column(db.String(50), unique=True, nullable = False, index=True)
    department = db.Column(db.String(100), index=True)
    phone = db.Column(db.String(20))
    cgpa = db.Column(db.Float)
    year_of_study = db.Column(db.Integer)
    skills = db.Column(db.Text)
    education = db.Column(db.Text)
    resume_path = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref = db.backref('student_profile', uselist=False))

    def __repr__(self):
        return f'<StudentProfile {self.name} ({self.roll_number})>'