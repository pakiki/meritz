from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models.scorecard import Scorecard, ScorecardCharacteristic, ScorecardAttribute
from backend.services.scorecard_service import ScorecardService
import json

scorecard_bp = Blueprint('scorecard', __name__)


@scorecard_bp.route('/scorecard', methods=['GET'])
def get_all_scorecards():
    scorecards = Scorecard.query.all()
    return jsonify([sc.to_dict() for sc in scorecards])


@scorecard_bp.route('/scorecard/<int:scorecard_id>', methods=['GET'])
def get_scorecard(scorecard_id):
    scorecard = Scorecard.query.get(scorecard_id)
    if not scorecard:
        return jsonify({'error': 'Scorecard not found'}), 404
    
    return jsonify(scorecard.to_dict())


@scorecard_bp.route('/scorecard', methods=['POST'])
def create_scorecard():
    data = request.json
    
    scorecard = Scorecard(
        name=data.get('name'),
        description=data.get('description'),
        base_score=data.get('base_score', 600),
        pdo=data.get('pdo', 20),
        base_odds=data.get('base_odds', 50),
        status='draft'
    )
    
    db.session.add(scorecard)
    db.session.commit()
    
    return jsonify(scorecard.to_dict()), 201


@scorecard_bp.route('/scorecard/<int:scorecard_id>/characteristic', methods=['POST'])
def add_characteristic(scorecard_id):
    scorecard = Scorecard.query.get(scorecard_id)
    if not scorecard:
        return jsonify({'error': 'Scorecard not found'}), 404
    
    data = request.json
    
    characteristic = ScorecardCharacteristic(
        scorecard_id=scorecard_id,
        name=data.get('name'),
        weight=data.get('weight'),
        order=data.get('order', 0)
    )
    
    db.session.add(characteristic)
    db.session.commit()
    
    return jsonify(characteristic.to_dict()), 201


@scorecard_bp.route('/scorecard/characteristic/<int:char_id>/attribute', methods=['POST'])
def add_attribute(char_id):
    characteristic = ScorecardCharacteristic.query.get(char_id)
    if not characteristic:
        return jsonify({'error': 'Characteristic not found'}), 404
    
    data = request.json
    
    scorecard = Scorecard.query.get(characteristic.scorecard_id)
    
    attribute = ScorecardAttribute(
        characteristic_id=char_id,
        attribute=data.get('attribute'),
        min_value=data.get('min_value'),
        max_value=data.get('max_value'),
        category=data.get('category'),
        good_count=data.get('good_count', 0),
        bad_count=data.get('bad_count', 0)
    )
    
    total_good = data.get('total_good', 1)
    total_bad = data.get('total_bad', 1)
    
    attribute.woe = ScorecardService.calculate_woe(
        attribute.good_count, attribute.bad_count, total_good, total_bad
    )
    attribute.iv = ScorecardService.calculate_iv(
        attribute.good_count, attribute.bad_count, total_good, total_bad
    )
    
    attribute.points = ScorecardService.calculate_scorecard_points(
        attribute.woe,
        characteristic.weight,
        scorecard.base_score,
        scorecard.pdo,
        scorecard.base_odds
    )
    
    db.session.add(attribute)
    db.session.commit()
    
    return jsonify(attribute.to_dict()), 201


@scorecard_bp.route('/scorecard/<int:scorecard_id>/calculate', methods=['POST'])
def calculate_score(scorecard_id):
    scorecard = Scorecard.query.get(scorecard_id)
    if not scorecard:
        return jsonify({'error': 'Scorecard not found'}), 404
    
    data = request.json
    input_data = data.get('input', {})
    
    result = ScorecardService.calculate_score(scorecard, input_data)
    
    probability = ScorecardService.calculate_probability(
        result['total_score'],
        scorecard.base_score,
        scorecard.pdo,
        scorecard.base_odds
    )
    
    return jsonify({
        'scorecard_id': scorecard_id,
        'scorecard_name': scorecard.name,
        'score': result['total_score'],
        'probability': round(probability, 4),
        'breakdown': result['breakdown'],
        'input': input_data
    })
