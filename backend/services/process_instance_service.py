from backend.models.process_instance import ProcessInstance
from backend.models.process_definition import ProcessDefinition
from backend.models.node_instance import NodeInstance
from backend.models.human_task import HumanTask
from backend.models.audit_log import AuditLog
from backend.models.workflow import Workflow
from backend.services.rule_engine_service import RuleEngineService
import json
import uuid
from datetime import datetime


class ProcessInstanceService:
    
    @staticmethod
    def start_process(process_definition_id, business_key, variables, started_by, db):
        process_def = db.session.query(ProcessDefinition).get(process_definition_id)
        if not process_def:
            return {'success': False, 'error': 'Process definition not found'}
        
        instance_id = f"PI-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
        
        process_instance = ProcessInstance(
            process_definition_id=process_definition_id,
            instance_id=instance_id,
            business_key=business_key,
            status='RUNNING',
            variables=json.dumps(variables),
            started_by=started_by
        )
        
        db.session.add(process_instance)
        db.session.commit()
        
        audit_log = AuditLog(
            process_instance_id=instance_id,
            event_type='PROCESS_STARTED',
            event_category='PROCESS',
            user_id=started_by,
            details=json.dumps({'variables': variables})
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return {
            'success': True,
            'process_instance': process_instance.to_dict()
        }
    
    @staticmethod
    def execute_workflow_as_process(workflow_id, input_data, db):
        workflow = db.session.query(Workflow).get(workflow_id)
        if not workflow:
            return {'success': False, 'error': 'Workflow not found'}
        
        instance_id = f"PI-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
        
        context = input_data.copy()
        context['workflow_id'] = workflow_id
        context['instance_id'] = instance_id
        
        start_time = datetime.utcnow()
        
        start_node = next((n for n in workflow.nodes if n.type == 'start'), None)
        if not start_node:
            return {'success': False, 'error': 'No start node found'}
        
        current_node = start_node
        visited_nodes = set()
        
        while current_node:
            if current_node.node_id in visited_nodes:
                break
            
            visited_nodes.add(current_node.node_id)
            
            node_start = datetime.utcnow()
            
            node_instance = NodeInstance(
                process_instance_id=instance_id,
                node_id=current_node.node_id,
                node_name=current_node.label or current_node.type,
                node_type=current_node.type,
                status='ACTIVE',
                variables=json.dumps(context)
            )
            db.session.add(node_instance)
            db.session.commit()
            
            result = ProcessInstanceService.execute_node(current_node, context, db)
            
            node_end = datetime.utcnow()
            node_instance.completion_time = node_end
            node_instance.duration_ms = int((node_end - node_start).total_seconds() * 1000)
            node_instance.status = 'COMPLETED'
            
            if not result.get('success'):
                node_instance.status = 'FAILED'
                node_instance.error_message = result.get('error')
                db.session.commit()
                
                return {
                    'success': False,
                    'error': result.get('error'),
                    'instance_id': instance_id,
                    'context': context
                }
            
            if result.get('output'):
                context.update(result['output'])
            
            db.session.commit()
            
            if current_node.type == 'end':
                break
            
            next_edge = next((e for e in workflow.edges if e.source == current_node.node_id), None)
            if not next_edge:
                break
            
            current_node = next((n for n in workflow.nodes if n.node_id == next_edge.target), None)
        
        end_time = datetime.utcnow()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        return {
            'success': True,
            'instance_id': instance_id,
            'status': 'COMPLETED',
            'duration_ms': duration_ms,
            'result': context
        }
    
    @staticmethod
    def execute_node(node, context, db):
        node_type = node.type
        config = json.loads(node.config) if node.config else {}
        
        if node_type == 'start':
            return {'success': True, 'output': {}}
        
        elif node_type == 'end':
            return {'success': True, 'output': {}}
        
        elif node_type == 'businessRule':
            rule_type = config.get('rule_type')
            rule_id = config.get('rule_id')
            
            if not rule_type or not rule_id:
                return {'success': False, 'error': 'Missing rule configuration'}
            
            result = RuleEngineService.execute_rule(rule_type, rule_id, context, db)
            
            if not result.get('success'):
                return result
            
            output = {}
            if 'score' in result:
                output['credit_score'] = result['score']
                output['probability'] = result.get('probability')
            if 'prediction' in result:
                output['prediction'] = result['prediction']
            if 'output' in result:
                output.update(result['output'])
            
            return {'success': True, 'output': output}
        
        elif node_type == 'gateway':
            condition = config.get('condition')
            
            if not condition:
                return {'success': True, 'output': {}}
            
            try:
                result = eval(condition, {"__builtins__": {}}, context)
                return {'success': True, 'output': {'gateway_result': result}}
            except Exception as e:
                return {'success': False, 'error': f'Gateway evaluation failed: {str(e)}'}
        
        elif node_type == 'userTask':
            task_id = f"TASK-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
            
            task = HumanTask(
                process_instance_id=context.get('instance_id'),
                task_id=task_id,
                name=config.get('name', node.label or 'User Task'),
                description=config.get('description'),
                form_key=config.get('form_key'),
                form_data=json.dumps(config.get('form_data', {})),
                assignee=config.get('assignee'),
                candidate_users=json.dumps(config.get('candidate_users', [])),
                candidate_groups=json.dumps(config.get('candidate_groups', []))
            )
            db.session.add(task)
            db.session.commit()
            
            return {'success': True, 'output': {'task_id': task_id, 'task_status': 'CREATED'}}
        
        elif node_type == 'serviceTask':
            service_name = config.get('service')
            
            return {'success': True, 'output': {'service_executed': service_name}}
        
        else:
            return {'success': True, 'output': {}}
    
    @staticmethod
    def get_process_instance(instance_id, db):
        instance = db.session.query(ProcessInstance).filter_by(instance_id=instance_id).first()
        if not instance:
            return None
        
        return instance.to_dict()
    
    @staticmethod
    def get_node_instances(process_instance_id, db):
        nodes = db.session.query(NodeInstance)\
            .filter_by(process_instance_id=process_instance_id)\
            .order_by(NodeInstance.trigger_time)\
            .all()
        
        return [n.to_dict() for n in nodes]
    
    @staticmethod
    def abort_process(instance_id, user_id, db):
        instance = db.session.query(ProcessInstance).filter_by(instance_id=instance_id).first()
        if not instance:
            return {'success': False, 'error': 'Process instance not found'}
        
        instance.status = 'ABORTED'
        instance.end_time = datetime.utcnow()
        
        if instance.start_time:
            instance.duration_ms = int((instance.end_time - instance.start_time).total_seconds() * 1000)
        
        db.session.commit()
        
        audit_log = AuditLog(
            process_instance_id=instance_id,
            event_type='PROCESS_ABORTED',
            event_category='PROCESS',
            user_id=user_id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return {'success': True, 'message': 'Process instance aborted'}
