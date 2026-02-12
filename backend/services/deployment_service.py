from backend.models.deployed_api import DeployedAPI
from backend.models.workflow import Workflow
from backend.services.api_generation_service import APIGenerationService
import json
from datetime import datetime


class DeploymentService:
    
    @staticmethod
    def deploy_workflow(workflow_id, db, version=None):
        workflow = db.session.query(Workflow).get(workflow_id)
        if not workflow:
            return {'success': False, 'error': 'Workflow not found'}
        
        api_name = APIGenerationService.generate_api_name(workflow)
        api_path = APIGenerationService.generate_api_path(api_name)
        
        existing_api = db.session.query(DeployedAPI).filter_by(api_path=api_path).first()
        if existing_api:
            return {
                'success': False,
                'error': f'API already deployed at {api_path}',
                'existing_deployment': existing_api.to_dict()
            }
        
        input_schema = APIGenerationService.extract_input_schema(workflow)
        output_schema = APIGenerationService.extract_output_schema(workflow)
        
        deployed_api = DeployedAPI(
            workflow_id=workflow_id,
            api_name=api_name,
            api_path=api_path,
            version=version or '1.0.0',
            description=workflow.description,
            input_schema=json.dumps(input_schema),
            output_schema=json.dumps(output_schema),
            status='active'
        )
        
        db.session.add(deployed_api)
        db.session.commit()
        
        swagger_spec = APIGenerationService.generate_swagger_spec(deployed_api, workflow)
        deployed_api.swagger_spec = json.dumps(swagger_spec)
        
        db.session.commit()
        
        return {
            'success': True,
            'deployment': deployed_api.to_dict(),
            'api_path': api_path,
            'swagger_url': f'/api/deployment/{deployed_api.id}/swagger'
        }
    
    @staticmethod
    def undeploy_api(deployment_id, db):
        deployed_api = db.session.query(DeployedAPI).get(deployment_id)
        if not deployed_api:
            return {'success': False, 'error': 'Deployment not found'}
        
        deployed_api.status = 'inactive'
        db.session.commit()
        
        return {
            'success': True,
            'message': f'API {deployed_api.api_name} has been undeployed'
        }
    
    @staticmethod
    def redeploy_api(deployment_id, db):
        deployed_api = db.session.query(DeployedAPI).get(deployment_id)
        if not deployed_api:
            return {'success': False, 'error': 'Deployment not found'}
        
        workflow = db.session.query(Workflow).get(deployed_api.workflow_id)
        if not workflow:
            return {'success': False, 'error': 'Associated workflow not found'}
        
        input_schema = APIGenerationService.extract_input_schema(workflow)
        output_schema = APIGenerationService.extract_output_schema(workflow)
        
        deployed_api.input_schema = json.dumps(input_schema)
        deployed_api.output_schema = json.dumps(output_schema)
        deployed_api.status = 'active'
        deployed_api.updated_at = datetime.utcnow()
        
        swagger_spec = APIGenerationService.generate_swagger_spec(deployed_api, workflow)
        deployed_api.swagger_spec = json.dumps(swagger_spec)
        
        db.session.commit()
        
        return {
            'success': True,
            'deployment': deployed_api.to_dict(),
            'message': f'API {deployed_api.api_name} has been redeployed'
        }
    
    @staticmethod
    def get_all_deployments(db):
        deployments = db.session.query(DeployedAPI).all()
        return [d.to_dict() for d in deployments]
    
    @staticmethod
    def get_deployment_by_path(api_path, db):
        deployed_api = db.session.query(DeployedAPI).filter_by(api_path=api_path, status='active').first()
        return deployed_api
    
    @staticmethod
    def update_execution_stats(deployment_id, db):
        deployed_api = db.session.query(DeployedAPI).get(deployment_id)
        if deployed_api:
            deployed_api.execution_count += 1
            deployed_api.last_executed_at = datetime.utcnow()
            db.session.commit()
