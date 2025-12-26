from flask import Blueprint, request, jsonify
from models.workflow import Workflow, WorkflowNode, WorkflowEdge
from services.workflow_service import WorkflowService
from database import db

bp = Blueprint('workflow', __name__)
workflow_service = WorkflowService()

@bp.route('/', methods=['GET'])
def get_workflows():
    """모든 워크플로우 조회"""
    try:
        workflows = Workflow.query.order_by(Workflow.updated_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [workflow.to_dict() for workflow in workflows]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/<int:workflow_id>', methods=['GET'])
def get_workflow(workflow_id):
    """특정 워크플로우 조회"""
    try:
        workflow = Workflow.query.get_or_404(workflow_id)
        return jsonify({
            'success': True,
            'data': workflow.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@bp.route('/', methods=['POST'])
def create_workflow():
    """워크플로우 생성"""
    try:
        data = request.json
        workflow = workflow_service.create_workflow(data)
        return jsonify({
            'success': True,
            'data': workflow.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@bp.route('/<int:workflow_id>', methods=['PUT'])
def update_workflow(workflow_id):
    """워크플로우 업데이트"""
    try:
        data = request.json
        workflow = workflow_service.update_workflow(workflow_id, data)
        return jsonify({
            'success': True,
            'data': workflow.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@bp.route('/<int:workflow_id>', methods=['DELETE'])
def delete_workflow(workflow_id):
    """워크플로우 삭제"""
    try:
        workflow_service.delete_workflow(workflow_id)
        return jsonify({
            'success': True,
            'message': 'Workflow deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@bp.route('/<int:workflow_id>/validate', methods=['POST'])
def validate_workflow(workflow_id):
    """워크플로우 검증"""
    try:
        result = workflow_service.validate_workflow(workflow_id)
        return jsonify({
            'success': True,
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
