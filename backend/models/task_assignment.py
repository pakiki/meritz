from datetime import datetime
from backend.database import db
import json


class TaskAssignment(db.Model):
    __tablename__ = 'task_assignment'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('human_task.id'), nullable=False)
    assignment_type = db.Column(db.String(50), nullable=False)
    assignee_id = db.Column(db.String(100), nullable=False)
    assignee_type = db.Column(db.String(50), default='USER')
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_by = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'assignment_type': self.assignment_type,
            'assignee_id': self.assignee_id,
            'assignee_type': self.assignee_type,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'assigned_by': self.assigned_by
        }
