from flask import Blueprint, request, jsonify
from models.rule import Rule
from services.engine_service import EngineService
from services.scoring_service import ScoringService
from database import db

bp = Blueprint('engine', __name__)
engine_service = EngineService()
scoring_service = ScoringService()

@bp.route('/rules', methods=['GET'])
def get_rules():
    """모든 규칙 조회"""
    try:
        rules = Rule.query.filter_by(is_active=True).order_by(Rule.priority.desc()).all()
        return jsonify({
            'success': True,
            'data': [rule.to_dict() for rule in rules]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/rules', methods=['POST'])
def create_rule():
    """규칙 생성"""
    try:
        data = request.json
        rule = Rule(
            name=data.get('name'),
            description=data.get('description'),
            rule_type=data.get('rule_type'),
            category=data.get('category'),
            condition=data.get('condition'),
            action=str(data.get('action', {})),
            priority=data.get('priority', 0),
            is_active=data.get('is_active', True)
        )
        db.session.add(rule)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': rule.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@bp.route('/rules/<int:rule_id>', methods=['PUT'])
def update_rule(rule_id):
    """규칙 업데이트"""
    try:
        rule = Rule.query.get_or_404(rule_id)
        data = request.json
        
        if 'name' in data:
            rule.name = data['name']
        if 'description' in data:
            rule.description = data['description']
        if 'condition' in data:
            rule.condition = data['condition']
        if 'action' in data:
            rule.action = str(data['action'])
        if 'priority' in data:
            rule.priority = data['priority']
        if 'is_active' in data:
            rule.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': rule.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@bp.route('/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    """규칙 삭제"""
    try:
        rule = Rule.query.get_or_404(rule_id)
        db.session.delete(rule)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Rule deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@bp.route('/score', methods=['POST'])
def calculate_score():
    """신용 점수 계산"""
    try:
        data = request.json
        score = scoring_service.calculate_score(data)
        
        return jsonify({
            'success': True,
            'data': {
                'score': score,
                'grade': scoring_service.get_credit_grade(score)
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
