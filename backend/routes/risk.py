from flask import Blueprint, request, jsonify
from models import RiskAssessment, Child, GrowthRecord, db
from routes.auth import token_required
from ai.growth_analyzer import GrowthAnalyzer
from datetime import datetime

risk_bp = Blueprint('risk', __name__, url_prefix='/api/risk')

analyzer = GrowthAnalyzer()

@risk_bp.route('/assessments', methods=['GET'])
@token_required
def get_all_risk_assessments(current_user):
    if current_user.role == 'doctor':
        assessments = RiskAssessment.query.all()
    else:
        child_ids = [child.id for child in Child.query.filter_by(user_id=current_user.id).all()]
        assessments = RiskAssessment.query.filter(RiskAssessment.child_id.in_(child_ids)).all()
    
    return jsonify({'assessments': [assessment.to_dict() for assessment in assessments]})

@risk_bp.route('/child/<int:child_id>', methods=['GET'])
@token_required
def get_risk_assessments(current_user, child_id):
    if current_user.role == 'doctor':
        child = Child.query.get(child_id)
    else:
        child = Child.query.filter_by(id=child_id, user_id=current_user.id).first()
    
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    assessments = RiskAssessment.query.filter_by(child_id=child_id).order_by(RiskAssessment.assessment_date.desc()).all()
    return jsonify({'assessments': [assessment.to_dict() for assessment in assessments]})

@risk_bp.route('/assess/<int:child_id>', methods=['POST'])
@token_required
def assess_risk_by_child(current_user, child_id):
    if current_user.role == 'doctor':
        child = Child.query.get(child_id)
    else:
        child = Child.query.filter_by(id=child_id, user_id=current_user.id).first()
    
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    record = GrowthRecord.query.filter_by(child_id=child_id).order_by(GrowthRecord.record_date.desc()).first()

    if not record:
        return jsonify({'error': 'No growth record found for this child'}), 404

    if not record.height or not record.weight:
        return jsonify({'error': 'Height and weight data are required for risk assessment'}), 400

    analysis_result = analyzer.analyze_growth(
        birth_date=child.birth_date,
        measure_date=record.record_date,
        height=float(record.height),
        weight=float(record.weight),
        gender=child.gender
    )

    new_assessment = RiskAssessment(
        child_id=child_id,
        stunting_risk=analysis_result['stunting_risk'],
        obesity_risk=analysis_result['obesity_risk'],
        details=analysis_result['details']
    )
    db.session.add(new_assessment)
    db.session.commit()

    return jsonify({
        'message': 'Risk assessment completed successfully',
        'assessment': new_assessment.to_dict(),
        'analysis': analysis_result
    }), 201

@risk_bp.route('', methods=['POST'])
@token_required
def create_risk_assessment(current_user):
    if current_user.role == 'doctor':
        return jsonify({'error': 'Doctors cannot create risk assessments'}), 403
    
    data = request.get_json()
    child_id = data.get('child_id')

    child = Child.query.filter_by(id=child_id, user_id=current_user.id).first()
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    new_assessment = RiskAssessment(
        child_id=child_id,
        stunting_risk=data.get('stunting_risk'),
        obesity_risk=data.get('obesity_risk'),
        details=data.get('details')
    )
    db.session.add(new_assessment)
    db.session.commit()
    return jsonify({'message': 'Risk assessment created successfully', 'assessment': new_assessment.to_dict()}), 201

@risk_bp.route('/<int:assessment_id>', methods=['GET'])
@token_required
def get_risk_assessment(current_user, assessment_id):
    assessment = RiskAssessment.query.get(assessment_id)
    if not assessment:
        return jsonify({'error': 'Assessment not found'}), 404

    if current_user.role == 'doctor':
        child = Child.query.get(assessment.child_id)
    else:
        child = Child.query.filter_by(id=assessment.child_id, user_id=current_user.id).first()
    
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    return jsonify({'assessment': assessment.to_dict()})

@risk_bp.route('/<int:assessment_id>', methods=['DELETE'])
@token_required
def delete_risk_assessment(current_user, assessment_id):
    if current_user.role == 'doctor':
        return jsonify({'error': 'Doctors cannot delete risk assessments'}), 403
    
    assessment = RiskAssessment.query.get(assessment_id)
    if not assessment:
        return jsonify({'error': 'Assessment not found'}), 404

    child = Child.query.filter_by(id=assessment.child_id, user_id=current_user.id).first()
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    db.session.delete(assessment)
    db.session.commit()
    return jsonify({'message': 'Risk assessment deleted successfully'})
