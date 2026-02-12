from datetime import datetime
from backend.database import db
import json


class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    process_instance_id = db.Column(db.String(255))
    task_id = db.Column(db.String(255))
    event_type = db.Column(db.String(100), nullable=False)
    event_category = db.Column(db.String(50), default='PROCESS')
    user_id = db.Column(db.String(100))
    details = db.Column(db.Text)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'process_instance_id': self.process_instance_id,
            'task_id': self.task_id,
            'event_type': self.event_type,
            'event_category': self.event_category,
            'user_id': self.user_id,
            'details': json.loads(self.details) if self.details else {},
            'old_value': self.old_value,
            'new_value': self.new_value,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
