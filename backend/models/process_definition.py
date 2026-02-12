from datetime import datetime
from backend.database import db
import json


class ProcessDefinition(db.Model):
    __tablename__ = 'process_definition'
    
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(50), default='1.0')
    description = db.Column(db.Text)
    bpmn_xml = db.Column(db.Text)
    process_variables = db.Column(db.Text)
    start_form = db.Column(db.Text)
    category = db.Column(db.String(100))
    status = db.Column(db.String(50), default='draft')
    deployed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    instances = db.relationship('ProcessInstance', backref='process_definition', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'bpmn_xml': self.bpmn_xml,
            'process_variables': json.loads(self.process_variables) if self.process_variables else [],
            'start_form': json.loads(self.start_form) if self.start_form else {},
            'category': self.category,
            'status': self.status,
            'deployed_at': self.deployed_at.isoformat() if self.deployed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
