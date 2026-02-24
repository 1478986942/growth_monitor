from models import db
from datetime import datetime

class Child(db.Model):
    __tablename__ = 'children'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    growth_records = db.relationship('GrowthRecord', backref='child', lazy=True, cascade='all, delete-orphan')
    risk_assessments = db.relationship('RiskAssessment', backref='child', lazy=True, cascade='all, delete-orphan')
    interventions = db.relationship('Intervention', backref='child', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }