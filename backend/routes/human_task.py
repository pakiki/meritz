from flask import Blueprint, request, jsonify
from backend.database import db
from backend.services.human_task_service import HumanTaskService

human_task_bp = Blueprint('human_task', __name__)


@human_task_bp.route('/task/my-tasks', methods=['GET'])
def get_my_tasks():
    user_id = request.args.get('user_id', 'user1')
    status = request.args.get('status')
    
    tasks = HumanTaskService.get_tasks_for_user(user_id, status, db)
    return jsonify(tasks)


@human_task_bp.route('/task/<task_id>', methods=['GET'])
def get_task_details(task_id):
    task = HumanTaskService.get_task_details(task_id, db)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task)


@human_task_bp.route('/task/<task_id>/claim', methods=['POST'])
def claim_task(task_id):
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    result = HumanTaskService.claim_task(task_id, user_id, db)
    
    if not result.get('success'):
        return jsonify(result), 400
    
    return jsonify(result)


@human_task_bp.route('/task/<task_id>/complete', methods=['POST'])
def complete_task(task_id):
    data = request.json
    user_id = data.get('user_id')
    output_data = data.get('output', {})
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    result = HumanTaskService.complete_task(task_id, user_id, output_data, db)
    
    if not result.get('success'):
        return jsonify(result), 400
    
    return jsonify(result)


@human_task_bp.route('/task/<task_id>/release', methods=['POST'])
def release_task(task_id):
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    result = HumanTaskService.release_task(task_id, user_id, db)
    
    if not result.get('success'):
        return jsonify(result), 400
    
    return jsonify(result)


@human_task_bp.route('/task/<task_id>/delegate', methods=['POST'])
def delegate_task(task_id):
    data = request.json
    from_user_id = data.get('from_user_id')
    to_user_id = data.get('to_user_id')
    
    if not from_user_id or not to_user_id:
        return jsonify({'error': 'from_user_id and to_user_id are required'}), 400
    
    result = HumanTaskService.delegate_task(task_id, from_user_id, to_user_id, db)
    
    if not result.get('success'):
        return jsonify(result), 400
    
    return jsonify(result)
