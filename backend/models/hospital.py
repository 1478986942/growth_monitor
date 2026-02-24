from models import db

class Hospital(db.Model):
    __tablename__ = 'hospitals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'address': self.address,
            'phone': self.phone,
            'description': self.description
        }
