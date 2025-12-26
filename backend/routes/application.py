from flask import Blueprint, request, jsonify
from models.application import Application, ApplicationLog
from services.workflow_service import WorkflowService
from services.engine_service import EngineService
from database import db

bp = Blueprint('application', __name__)
workflow_service = WorkflowService()
engine_service = EngineService()

@bp.route('/', methods=['GET'])
def get_applications():
    """모든 신청서 조회"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', None)
        
        query = Application.query
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(Application.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [app.to_dict() for app in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/<int:application_id>', methods=['GET'])
def get_application(application_id):
    """특정 신청서 조회"""
    try:
        application = Application.query.get_or_404(application_id)
        return jsonify({
            'success': True,
            'data': application.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@bp.route('/', methods=['POST'])
def create_application():
    """신청서 생성 및 실행"""
    try:
        data = request.json
        workflow_id = data.get('workflow_id')
        application_data = data.get('application_data', {})
        
        if not workflow_id:
            return jsonify({
                'success': False,
                'error': 'workflow_id is required'
            }), 400
        
        # 신청서 생성
        application = Application(
            workflow_id=workflow_id,
            applicant_name=application_data.get('applicant_name'),
            applicant_id=application_data.get('applicant_id'),
            application_data=str(application_data),
            status='pending'
        )
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': application.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@bp.route('/<int:application_id>/execute', methods=['POST'])
def execute_application(application_id):
    """신청서 실행"""
    try:
        result = engine_service.execute_workflow(application_id)
        return jsonify({
            'success': True,
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@bp.route('/<int:application_id>/logs', methods=['GET'])
def get_application_logs(application_id):
    """신청서 실행 로그 조회"""
    try:
        logs = ApplicationLog.query.filter_by(application_id=application_id)\
            .order_by(ApplicationLog.created_at.asc()).all()
        return jsonify({
            'success': True,
            'data': [log.to_dict() for log in logs]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
