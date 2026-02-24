from models import db
from datetime import datetime

class RiskAssessment(db.Model):
    __tablename__ = 'risk_assessments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id', ondelete='CASCADE'), nullable=False)
    assessment_date = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    stunting_risk = db.Column(db.DECIMAL(5, 2), comment='矮小症风险概率%')
    obesity_risk = db.Column(db.DECIMAL(5, 2), comment='肥胖风险概率%')
    details = db.Column(db.JSON, comment='详细风险因子')

    interventions = db.relationship('Intervention', backref='assessment', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None,
            'stunting_risk': float(self.stunting_risk) if self.stunting_risk else None,
            'obesity_risk': float(self.obesity_risk) if self.obesity_risk else None,
            'details': self.details
        }
