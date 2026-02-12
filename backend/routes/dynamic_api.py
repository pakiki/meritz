from flask import Blueprint, request, jsonify
from backend.database import db
from backend.services.deployment_service import DeploymentService
from backend.services.process_instance_service import ProcessInstanceService

dynamic_api_bp = Blueprint('dynamic_api', __name__)


@dynamic_api_bp.route('/execute/<path:api_name>', methods=['POST', 'GET'])
def execute_dynamic_api(api_name):
    api_path = f'/api/execute/{api_name}'
    
    deployed_api = DeploymentService.get_deployment_by_path(api_path, db)
    
    if not deployed_api:
        return jsonify({'error': f'API not found: {api_path}'}), 404
    
    if deployed_api.status != 'active':
        return jsonify({'error': 'API is not active'}), 403
    
    if request.method == 'GET':
        return jsonify({
            'api_name': deployed_api.api_name,
            'version': deployed_api.version,
            'status': deployed_api.status,
            'description': deployed_api.description,
            'execution_count': deployed_api.execution_count,
            'input_schema': deployed_api.to_dict().get('input_schema', {}),
            'output_schema': deployed_api.to_dict().get('output_schema', {})
        })
    
    input_data = request.json or {}
    
    result = ProcessInstanceService.execute_workflow_as_process(
        deployed_api.workflow_id,
        input_data,
        db
    )
    
    DeploymentService.update_execution_stats(deployed_api.id, db)
    
    if not result.get('success'):
        return jsonify(result), 500
    
    return jsonify(result)
