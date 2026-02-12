from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models.process_instance import ProcessInstance
from backend.services.process_instance_service import ProcessInstanceService

process_instance_bp = Blueprint('process_instance', __name__)


@process_instance_bp.route('/process-instance', methods=['GET'])
def get_all_instances():
    instances = ProcessInstance.query.order_by(ProcessInstance.start_time.desc()).limit(100).all()
    return jsonify([inst.to_dict() for inst in instances])


@process_instance_bp.route('/process-instance/<instance_id>', methods=['GET'])
def get_instance(instance_id):
    instance_data = ProcessInstanceService.get_process_instance(instance_id, db)
    
    if not instance_data:
        return jsonify({'error': 'Process instance not found'}), 404
    
    node_instances = ProcessInstanceService.get_node_instances(instance_id, db)
    instance_data['node_instances'] = node_instances
    
    return jsonify(instance_data)


@process_instance_bp.route('/process-instance/<instance_id>/abort', methods=['POST'])
def abort_instance(instance_id):
    data = request.json
    user_id = data.get('user_id', 'system')
    
    result = ProcessInstanceService.abort_process(instance_id, user_id, db)
    
    if not result.get('success'):
        return jsonify(result), 404
    
    return jsonify(result)


@process_instance_bp.route('/process-instance/execute', methods=['POST'])
def execute_process():
    data = request.json
    
    workflow_id = data.get('workflow_id')
    input_data = data.get('input', {})
    
    if not workflow_id:
        return jsonify({'error': 'workflow_id is required'}), 400
    
    result = ProcessInstanceService.execute_workflow_as_process(workflow_id, input_data, db)
    
    if not result.get('success'):
        return jsonify(result), 500
    
    return jsonify(result)
