from models import db
from datetime import datetime

class GrowthRecord(db.Model):
    __tablename__ = 'growth_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id', ondelete='CASCADE'), nullable=False)
    record_date = db.Column(db.Date, nullable=False)
    height = db.Column(db.DECIMAL(5, 2), comment='单位cm')
    weight = db.Column(db.DECIMAL(5, 2), comment='单位kg')
    bmi = db.Column(db.DECIMAL(4, 2), server_default=db.text('0'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'height': float(self.height) if self.height else None,
            'weight': float(self.weight) if self.weight else None,
            'bmi': float(self.bmi) if self.bmi else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
