from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models.deployed_api import DeployedAPI
from backend.models.workflow import Workflow
from backend.services.deployment_service import DeploymentService
from backend.services.testing_service import TestingService
from backend.services.process_instance_service import ProcessInstanceService
import json

deployment_bp = Blueprint('deployment', __name__)


@deployment_bp.route('/deployment', methods=['GET'])
def get_all_deployments():
    deployments = DeploymentService.get_all_deployments(db)
    return jsonify(deployments)


@deployment_bp.route('/deployment/<int:deployment_id>', methods=['GET'])
def get_deployment(deployment_id):
    deployment = DeployedAPI.query.get(deployment_id)
    if not deployment:
        return jsonify({'error': 'Deployment not found'}), 404
    
    return jsonify(deployment.to_dict())


@deployment_bp.route('/deployment/workflow/<int:workflow_id>', methods=['POST'])
def deploy_workflow(workflow_id):
    data = request.json or {}
    version = data.get('version')
    
    result = DeploymentService.deploy_workflow(workflow_id, db, version)
    
    if not result.get('success'):
        return jsonify(result), 400
    
    return jsonify(result), 201


@deployment_bp.route('/deployment/<int:deployment_id>', methods=['DELETE'])
def undeploy_api(deployment_id):
    result = DeploymentService.undeploy_api(deployment_id, db)
    
    if not result.get('success'):
        return jsonify(result), 404
    
    return jsonify(result)


@deployment_bp.route('/deployment/<int:deployment_id>/redeploy', methods=['POST'])
def redeploy_api(deployment_id):
    result = DeploymentService.redeploy_api(deployment_id, db)
    
    if not result.get('success'):
        return jsonify(result), 404
    
    return jsonify(result)


@deployment_bp.route('/deployment/<int:deployment_id>/swagger', methods=['GET'])
def get_swagger_spec(deployment_id):
    deployment = DeployedAPI.query.get(deployment_id)
    if not deployment:
        return jsonify({'error': 'Deployment not found'}), 404
    
    swagger_spec = json.loads(deployment.swagger_spec) if deployment.swagger_spec else {}
    return jsonify(swagger_spec)


@deployment_bp.route('/deployment/<int:deployment_id>/test-case', methods=['POST'])
def create_test_case(deployment_id):
    deployment = DeployedAPI.query.get(deployment_id)
    if not deployment:
        return jsonify({'error': 'Deployment not found'}), 404
    
    data = request.json
    
    test_case = TestingService.create_test_case(
        deployment_id,
        data.get('name'),
        data.get('description'),
        data.get('input_data', {}),
        data.get('expected_output'),
        db
    )
    
    return jsonify(test_case), 201


@deployment_bp.route('/deployment/<int:deployment_id>/test', methods=['POST'])
def test_deployment(deployment_id):
    deployment = DeployedAPI.query.get(deployment_id)
    if not deployment:
        return jsonify({'error': 'Deployment not found'}), 404
    
    data = request.json
    input_data = data.get('input', {})
    
    def execute_workflow(workflow_id, input_data):
        return ProcessInstanceService.execute_workflow_as_process(workflow_id, input_data, db)
    
    result = execute_workflow(deployment.workflow_id, input_data)
    
    DeploymentService.update_execution_stats(deployment_id, db)
    
    return jsonify(result)


@deployment_bp.route('/deployment/<int:deployment_id>/test-case/<int:test_case_id>/execute', methods=['POST'])
def execute_test_case(deployment_id, test_case_id):
    def execute_workflow(workflow_id, input_data):
        return ProcessInstanceService.execute_workflow_as_process(workflow_id, input_data, db)
    
    result = TestingService.execute_test_case(test_case_id, execute_workflow, db)
    
    if not result.get('success'):
        return jsonify(result), 400
    
    return jsonify(result)
