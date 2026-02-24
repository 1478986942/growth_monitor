from flask import Blueprint, jsonify
from models import Hospital, db

hospital_bp = Blueprint('hospital', __name__, url_prefix='/api/hospital')

@hospital_bp.route('', methods=['GET'])
def get_hospitals():
    hospitals = Hospital.query.all()
    return jsonify({'hospitals': [hospital.to_dict() for hospital in hospitals]})

@hospital_bp.route('', methods=['POST'])
def create_hospital():
    from flask import request
    data = request.get_json()
    new_hospital = Hospital(
        name=data.get('name'),
        department=data.get('department'),
        address=data.get('address'),
        phone=data.get('phone'),
        description=data.get('description')
    )
    db.session.add(new_hospital)
    db.session.commit()
    return jsonify({'message': 'Hospital created successfully', 'hospital': new_hospital.to_dict()}), 201

@hospital_bp.route('/<int:hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        return jsonify({'error': 'Hospital not found'}), 404
    return jsonify({'hospital': hospital.to_dict()})
