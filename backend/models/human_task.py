from datetime import datetime
from backend.database import db
import json


class HumanTask(db.Model):
    __tablename__ = 'human_task'
    
    id = db.Column(db.Integer, primary_key=True)
    process_instance_id = db.Column(db.Integer, db.ForeignKey('process_instance.id'), nullable=False)
    task_id = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    task_type = db.Column(db.String(50), default='USER_TASK')
    status = db.Column(db.String(50), default='READY')
    priority = db.Column(db.Integer, default=0)
    form_key = db.Column(db.String(255))
    form_data = db.Column(db.Text)
    assignee = db.Column(db.String(100))
    owner = db.Column(db.String(100))
    candidate_users = db.Column(db.Text)
    candidate_groups = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    claimed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    assignments = db.relationship('TaskAssignment', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'process_instance_id': self.process_instance_id,
            'task_id': self.task_id,
            'name': self.name,
            'description': self.description,
            'task_type': self.task_type,
            'status': self.status,
            'priority': self.priority,
            'form_key': self.form_key,
            'form_data': json.loads(self.form_data) if self.form_data else {},
            'assignee': self.assignee,
            'owner': self.owner,
            'candidate_users': json.loads(self.candidate_users) if self.candidate_users else [],
            'candidate_groups': json.loads(self.candidate_groups) if self.candidate_groups else [],
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'claimed_at': self.claimed_at.isoformat() if self.claimed_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
