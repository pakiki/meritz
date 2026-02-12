from datetime import datetime
from backend.database import db
import json


class ProcessInstance(db.Model):
    __tablename__ = 'process_instance'
    
    id = db.Column(db.Integer, primary_key=True)
    process_definition_id = db.Column(db.Integer, db.ForeignKey('process_definition.id'), nullable=False)
    instance_id = db.Column(db.String(255), nullable=False, unique=True)
    business_key = db.Column(db.String(255))
    status = db.Column(db.String(50), default='RUNNING')
    variables = db.Column(db.Text)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration_ms = db.Column(db.Integer)
    started_by = db.Column(db.String(100))
    parent_instance_id = db.Column(db.String(255))
    super_process_instance_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    node_instances = db.relationship('NodeInstance', backref='process_instance', lazy=True, cascade='all, delete-orphan')
    tasks = db.relationship('HumanTask', backref='process_instance', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'process_definition_id': self.process_definition_id,
            'instance_id': self.instance_id,
            'business_key': self.business_key,
            'status': self.status,
            'variables': json.loads(self.variables) if self.variables else {},
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_ms': self.duration_ms,
            'started_by': self.started_by,
            'parent_instance_id': self.parent_instance_id,
            'super_process_instance_id': self.super_process_instance_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
