from datetime import datetime
from backend.database import db
import json


class NodeInstance(db.Model):
    __tablename__ = 'node_instance'
    
    id = db.Column(db.Integer, primary_key=True)
    process_instance_id = db.Column(db.Integer, db.ForeignKey('process_instance.id'), nullable=False)
    node_id = db.Column(db.String(255), nullable=False)
    node_name = db.Column(db.String(255))
    node_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='ACTIVE')
    trigger_time = db.Column(db.DateTime, default=datetime.utcnow)
    completion_time = db.Column(db.DateTime)
    duration_ms = db.Column(db.Integer)
    variables = db.Column(db.Text)
    error_message = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'process_instance_id': self.process_instance_id,
            'node_id': self.node_id,
            'node_name': self.node_name,
            'node_type': self.node_type,
            'status': self.status,
            'trigger_time': self.trigger_time.isoformat() if self.trigger_time else None,
            'completion_time': self.completion_time.isoformat() if self.completion_time else None,
            'duration_ms': self.duration_ms,
            'variables': json.loads(self.variables) if self.variables else {},
            'error_message': self.error_message
        }
