from flask import Blueprint, request, jsonify
from models import GrowthRecord, Child, db
from routes.auth import token_required

growth_bp = Blueprint('growth', __name__, url_prefix='/api/growth')

@growth_bp.route('/records', methods=['GET'])
@token_required
def get_all_growth_records(current_user):
    if current_user.role == 'doctor':
        records = GrowthRecord.query.all()
    else:
        child_ids = [child.id for child in Child.query.filter_by(user_id=current_user.id).all()]
        records = GrowthRecord.query.filter(GrowthRecord.child_id.in_(child_ids)).all()
    
    return jsonify({'records': [record.to_dict() for record in records]})

@growth_bp.route('/child/<int:child_id>', methods=['GET'])
@token_required
def get_growth_records(current_user, child_id):
    if current_user.role == 'doctor':
        child = Child.query.get(child_id)
    else:
        child = Child.query.filter_by(id=child_id, user_id=current_user.id).first()
    
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    records = GrowthRecord.query.filter_by(child_id=child_id).order_by(GrowthRecord.record_date).all()
    return jsonify({'records': [record.to_dict() for record in records]})

@growth_bp.route('', methods=['POST'])
@token_required
def create_growth_record(current_user):
    if current_user.role == 'doctor':
        return jsonify({'error': 'Doctors cannot create growth records'}), 403
    
    data = request.get_json()
    child_id = data.get('child_id')

    child = Child.query.filter_by(id=child_id, user_id=current_user.id).first()
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    height = data.get('height')
    weight = data.get('weight')

    new_record = GrowthRecord(
        child_id=child_id,
        record_date=data.get('record_date'),
        height=height,
        weight=weight
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'message': 'Growth record created successfully', 'record': new_record.to_dict()}), 201

@growth_bp.route('/<int:record_id>', methods=['PUT'])
@token_required
def update_growth_record(current_user, record_id):
    if current_user.role == 'doctor':
        return jsonify({'error': 'Doctors cannot update growth records'}), 403
    
    record = GrowthRecord.query.get(record_id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404

    child = Child.query.filter_by(id=record.child_id, user_id=current_user.id).first()
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    data = request.get_json()
    if 'record_date' in data:
        record.record_date = data['record_date']
    if 'height' in data:
        record.height = data['height']
    if 'weight' in data:
        record.weight = data['weight']

    db.session.commit()
    return jsonify({'message': 'Growth record updated successfully', 'record': record.to_dict()})

@growth_bp.route('/<int:record_id>', methods=['DELETE'])
@token_required
def delete_growth_record(current_user, record_id):
    if current_user.role == 'doctor':
        return jsonify({'error': 'Doctors cannot delete growth records'}), 403
    
    record = GrowthRecord.query.get(record_id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404

    child = Child.query.filter_by(id=record.child_id, user_id=current_user.id).first()
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Growth record deleted successfully'})
