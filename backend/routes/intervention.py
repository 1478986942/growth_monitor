from flask import Blueprint, request, jsonify
from models import Intervention, Child, RiskAssessment, db
from routes.auth import token_required
from ai.growth_analyzer import GrowthAnalyzer
from datetime import datetime, timedelta

intervention_bp = Blueprint('intervention', __name__, url_prefix='/api/intervention')

analyzer = GrowthAnalyzer()

@intervention_bp.route('/interventions', methods=['GET'])
@token_required
def get_all_interventions(current_user):
    if current_user.role == 'doctor':
        interventions = Intervention.query.all()
    else:
        child_ids = [child.id for child in Child.query.filter_by(user_id=current_user.id).all()]
        interventions = Intervention.query.filter(Intervention.child_id.in_(child_ids)).all()
    
    return jsonify({'interventions': [intervention.to_dict() for intervention in interventions]})

@intervention_bp.route('/child/<int:child_id>', methods=['GET'])
@token_required
def get_interventions(current_user, child_id):
    if current_user.role == 'doctor':
        child = Child.query.get(child_id)
    else:
        child = Child.query.filter_by(id=child_id, user_id=current_user.id).first()
    
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    interventions = Intervention.query.filter_by(child_id=child_id).order_by(Intervention.created_at.desc()).all()
    return jsonify({'interventions': [intervention.to_dict() for intervention in interventions]})

@intervention_bp.route('/generate', methods=['POST'])
@token_required
def generate_intervention(current_user):
    data = request.get_json()
    assessment_id = data.get('assessment_id')

    assessment = RiskAssessment.query.get(assessment_id)
    if not assessment:
        return jsonify({'error': 'Assessment not found'}), 404

    if current_user.role == 'parent':
        child = Child.query.filter_by(id=assessment.child_id, user_id=current_user.id).first()
    else:
        child = Child.query.get(assessment.child_id)
    
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    risk_assessment = {
        'stunting_risk': assessment.stunting_risk,
        'obesity_risk': assessment.obesity_risk,
        'details': assessment.details
    }

    intervention_plan = analyzer.generate_intervention_plan(risk_assessment)

    plan_content = '\n\n'.join([
        f"【{item['priority'].upper()} - {item['category']}】{item['title']}\n{item['content']}"
        for item in intervention_plan['interventions']
    ])

    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=90)

    new_intervention = Intervention(
        child_id=child.id,
        assessment_id=assessment_id,
        plan_title=f"基于风险评估的个性化干预方案 - {datetime.now().strftime('%Y-%m-%d')}",
        plan_content=plan_content,
        start_date=start_date,
        end_date=end_date,
        status='pending'
    )
    db.session.add(new_intervention)
    db.session.commit()

    return jsonify({
        'message': 'Intervention plan generated successfully',
        'intervention': new_intervention.to_dict(),
        'plan_details': intervention_plan
    }), 201

@intervention_bp.route('', methods=['POST'])
@token_required
def create_intervention(current_user):
    data = request.get_json()
    child_id = data.get('child_id')

    if current_user.role == 'parent':
        child = Child.query.filter_by(id=child_id, user_id=current_user.id).first()
    else:
        child = Child.query.get(child_id)
    
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    new_intervention = Intervention(
        child_id=child_id,
        assessment_id=data.get('assessment_id'),
        plan_title=data.get('plan_title'),
        plan_content=data.get('plan_content'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        status=data.get('status', 'pending')
    )
    db.session.add(new_intervention)
    db.session.commit()
    return jsonify({'message': 'Intervention created successfully', 'intervention': new_intervention.to_dict()}), 201

@intervention_bp.route('/<int:intervention_id>', methods=['GET'])
@token_required
def get_intervention(current_user, intervention_id):
    if current_user.role == 'doctor':
        intervention = Intervention.query.get(intervention_id)
    else:
        intervention = Intervention.query.get(intervention_id)
        if intervention:
            child = Child.query.filter_by(id=intervention.child_id, user_id=current_user.id).first()
            if not child:
                return jsonify({'error': 'Child not found'}), 404
    
    if not intervention:
        return jsonify({'error': 'Intervention not found'}), 404

    return jsonify({'intervention': intervention.to_dict()})

@intervention_bp.route('/<int:intervention_id>', methods=['PUT'])
@token_required
def update_intervention(current_user, intervention_id):
    intervention = Intervention.query.get(intervention_id)
    if not intervention:
        return jsonify({'error': 'Intervention not found'}), 404

    if current_user.role == 'parent':
        child = Child.query.filter_by(id=intervention.child_id, user_id=current_user.id).first()
        if not child:
            return jsonify({'error': 'Child not found'}), 404

    data = request.get_json()
    if 'plan_title' in data:
        intervention.plan_title = data['plan_title']
    if 'plan_content' in data:
        intervention.plan_content = data['plan_content']
    if 'start_date' in data:
        intervention.start_date = data['start_date']
    if 'end_date' in data:
        intervention.end_date = data['end_date']
    if 'status' in data:
        intervention.status = data['status']

    db.session.commit()
    return jsonify({'message': 'Intervention updated successfully', 'intervention': intervention.to_dict()})

@intervention_bp.route('/<int:intervention_id>/status', methods=['PATCH'])
@token_required
def update_intervention_status(current_user, intervention_id):
    intervention = Intervention.query.get(intervention_id)
    if not intervention:
        return jsonify({'error': 'Intervention not found'}), 404

    if current_user.role == 'parent':
        child = Child.query.filter_by(id=intervention.child_id, user_id=current_user.id).first()
        if not child:
            return jsonify({'error': 'Child not found'}), 404

    data = request.get_json()
    status = data.get('status')

    if status not in ['pending', 'ongoing', 'completed']:
        return jsonify({'error': 'Invalid status. Must be pending, ongoing, or completed'}), 400

    intervention.status = status
    db.session.commit()

    return jsonify({'message': 'Intervention status updated successfully', 'intervention': intervention.to_dict()})

@intervention_bp.route('/<int:intervention_id>', methods=['DELETE'])
@token_required
def delete_intervention(current_user, intervention_id):
    intervention = Intervention.query.get(intervention_id)
    if not intervention:
        return jsonify({'error': 'Intervention not found'}), 404

    if current_user.role == 'parent':
        child = Child.query.filter_by(id=intervention.child_id, user_id=current_user.id).first()
        if not child:
            return jsonify({'error': 'Child not found'}), 404

    db.session.delete(intervention)
    db.session.commit()
    return jsonify({'message': 'Intervention deleted successfully'})
