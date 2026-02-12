from backend.models.human_task import HumanTask
from backend.models.task_assignment import TaskAssignment
from backend.models.audit_log import AuditLog
from datetime import datetime
import json


class HumanTaskService:
    
    @staticmethod
    def get_tasks_for_user(user_id, status=None, db=None):
        query = db.session.query(HumanTask)
        
        if status:
            query = query.filter(HumanTask.status == status)
        else:
            query = query.filter(HumanTask.status.in_(['READY', 'RESERVED']))
        
        query = query.filter(
            (HumanTask.assignee == user_id) |
            (HumanTask.candidate_users.contains(f'"{user_id}"'))
        )
        
        tasks = query.order_by(HumanTask.priority.desc(), HumanTask.created_at).all()
        
        return [task.to_dict() for task in tasks]
    
    @staticmethod
    def claim_task(task_id, user_id, db):
        task = db.session.query(HumanTask).filter_by(task_id=task_id).first()
        if not task:
            return {'success': False, 'error': 'Task not found'}
        
        if task.status != 'READY':
            return {'success': False, 'error': f'Task cannot be claimed, current status: {task.status}'}
        
        candidate_users = json.loads(task.candidate_users) if task.candidate_users else []
        
        if task.assignee and task.assignee != user_id:
            return {'success': False, 'error': 'Task already assigned to another user'}
        
        if candidate_users and user_id not in candidate_users:
            return {'success': False, 'error': 'User not in candidate list'}
        
        task.assignee = user_id
        task.status = 'RESERVED'
        task.claimed_at = datetime.utcnow()
        
        assignment = TaskAssignment(
            task_id=task.id,
            assignment_type='CLAIM',
            assignee_id=user_id,
            assignee_type='USER',
            assigned_by=user_id
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        audit_log = AuditLog(
            task_id=task_id,
            event_type='TASK_CLAIMED',
            event_category='TASK',
            user_id=user_id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return {'success': True, 'task': task.to_dict()}
    
    @staticmethod
    def complete_task(task_id, user_id, output_data, db):
        task = db.session.query(HumanTask).filter_by(task_id=task_id).first()
        if not task:
            return {'success': False, 'error': 'Task not found'}
        
        if task.assignee != user_id:
            return {'success': False, 'error': 'Task not assigned to this user'}
        
        if task.status not in ['RESERVED', 'IN_PROGRESS']:
            return {'success': False, 'error': f'Task cannot be completed, current status: {task.status}'}
        
        task.status = 'COMPLETED'
        task.completed_at = datetime.utcnow()
        
        if output_data:
            current_form_data = json.loads(task.form_data) if task.form_data else {}
            current_form_data.update(output_data)
            task.form_data = json.dumps(current_form_data)
        
        db.session.commit()
        
        audit_log = AuditLog(
            task_id=task_id,
            event_type='TASK_COMPLETED',
            event_category='TASK',
            user_id=user_id,
            details=json.dumps(output_data) if output_data else None
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return {'success': True, 'task': task.to_dict(), 'output': output_data}
    
    @staticmethod
    def release_task(task_id, user_id, db):
        task = db.session.query(HumanTask).filter_by(task_id=task_id).first()
        if not task:
            return {'success': False, 'error': 'Task not found'}
        
        if task.assignee != user_id:
            return {'success': False, 'error': 'Task not assigned to this user'}
        
        task.assignee = None
        task.status = 'READY'
        task.claimed_at = None
        
        db.session.commit()
        
        audit_log = AuditLog(
            task_id=task_id,
            event_type='TASK_RELEASED',
            event_category='TASK',
            user_id=user_id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return {'success': True, 'task': task.to_dict()}
    
    @staticmethod
    def delegate_task(task_id, from_user_id, to_user_id, db):
        task = db.session.query(HumanTask).filter_by(task_id=task_id).first()
        if not task:
            return {'success': False, 'error': 'Task not found'}
        
        if task.assignee != from_user_id:
            return {'success': False, 'error': 'Task not assigned to this user'}
        
        old_assignee = task.assignee
        task.assignee = to_user_id
        task.owner = from_user_id
        
        assignment = TaskAssignment(
            task_id=task.id,
            assignment_type='DELEGATE',
            assignee_id=to_user_id,
            assignee_type='USER',
            assigned_by=from_user_id
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        audit_log = AuditLog(
            task_id=task_id,
            event_type='TASK_DELEGATED',
            event_category='TASK',
            user_id=from_user_id,
            old_value=old_assignee,
            new_value=to_user_id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return {'success': True, 'task': task.to_dict()}
    
    @staticmethod
    def get_task_details(task_id, db):
        task = db.session.query(HumanTask).filter_by(task_id=task_id).first()
        if not task:
            return None
        
        task_dict = task.to_dict()
        
        assignments = db.session.query(TaskAssignment)\
            .filter_by(task_id=task.id)\
            .order_by(TaskAssignment.assigned_at.desc())\
            .all()
        
        task_dict['assignments'] = [a.to_dict() for a in assignments]
        
        audit_logs = db.session.query(AuditLog)\
            .filter_by(task_id=task_id)\
            .order_by(AuditLog.timestamp.desc())\
            .all()
        
        task_dict['history'] = [log.to_dict() for log in audit_logs]
        
        return task_dict
    
    @staticmethod
    def get_tasks_by_process(process_instance_id, db):
        tasks = db.session.query(HumanTask)\
            .filter_by(process_instance_id=process_instance_id)\
            .order_by(HumanTask.created_at)\
            .all()
        
        return [task.to_dict() for task in tasks]
