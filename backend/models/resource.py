from models import db
from datetime import datetime

class Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    category = db.Column(db.Enum('nutrition', 'growth', 'health', 'psychology', 'parenting', 'medical', 'emergency', 'development'), nullable=False)
    content = db.Column(db.Text)
    link = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'content': self.content,
            'link': self.link,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
