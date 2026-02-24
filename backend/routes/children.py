from flask import Blueprint, request, jsonify
from models import Child, db
from routes.auth import token_required, doctor_or_parent_required

children_bp = Blueprint('children', __name__, url_prefix='/api/children')

@children_bp.route('', methods=['GET'])
@token_required
def get_children(current_user):
    if current_user.role == 'doctor':
        children = Child.query.all()
    else:
        children = Child.query.filter_by(user_id=current_user.id).all()
    return jsonify({'children': [child.to_dict() for child in children]})

@children_bp.route('', methods=['POST'])
@token_required
def create_child(current_user):
    if current_user.role == 'doctor':
        return jsonify({'error': 'Doctors cannot create children'}), 403
    
    data = request.get_json()
    new_child = Child(
        user_id=current_user.id,
        name=data.get('name'),
        gender=data.get('gender'),
        birth_date=data.get('birth_date')
    )
    db.session.add(new_child)
    db.session.commit()
    return jsonify({'message': 'Child created successfully', 'child': new_child.to_dict()}), 201

@children_bp.route('/<int:child_id>', methods=['GET'])
@token_required
def get_child(current_user, child_id):
    if current_user.role == 'doctor':
        child = Child.query.get(child_id)
    else:
        child = Child.query.filter_by(id=child_id, user_id=current_user.id).first()
    
    if not child:
        return jsonify({'error': 'Child not found'}), 404
    return jsonify({'child': child.to_dict()})

@children_bp.route('/<int:child_id>', methods=['PUT'])
@token_required
def update_child(current_user, child_id):
    if current_user.role == 'doctor':
        return jsonify({'error': 'Doctors cannot update children'}), 403
    
    child = Child.query.filter_by(id=child_id, user_id=current_user.id).first()
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    data = request.get_json()
    if 'name' in data:
        child.name = data['name']
    if 'gender' in data:
        child.gender = data['gender']
    if 'birth_date' in data:
        child.birth_date = data['birth_date']

    db.session.commit()
    return jsonify({'message': 'Child updated successfully', 'child': child.to_dict()})

@children_bp.route('/<int:child_id>', methods=['DELETE'])
@token_required
def delete_child(current_user, child_id):
    if current_user.role == 'doctor':
        return jsonify({'error': 'Doctors cannot delete children'}), 403
    
    child = Child.query.filter_by(id=child_id, user_id=current_user.id).first()
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    db.session.delete(child)
    db.session.commit()
    return jsonify({'message': 'Child deleted successfully'})
