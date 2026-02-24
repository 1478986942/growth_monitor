from flask import Blueprint, request, jsonify
from models import Resource, db

resource_bp = Blueprint('resource', __name__, url_prefix='/api/resource')

@resource_bp.route('', methods=['GET'])
def get_resources():
    category = request.args.get('category')
    query = Resource.query
    if category:
        query = query.filter_by(category=category)
    resources = query.all()
    return jsonify({'resources': [resource.to_dict() for resource in resources]})

@resource_bp.route('', methods=['POST'])
def create_resource():
    data = request.get_json()
    new_resource = Resource(
        title=data.get('title'),
        category=data.get('category'),
        content=data.get('content'),
        link=data.get('link')
    )
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({'message': 'Resource created successfully', 'resource': new_resource.to_dict()}), 201

@resource_bp.route('/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({'error': 'Resource not found'}), 404
    return jsonify({'resource': resource.to_dict()})
