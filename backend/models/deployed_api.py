from datetime import datetime
from backend.database import db
import json


class DeployedAPI(db.Model):
    __tablename__ = 'deployed_api'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'), nullable=False)
    api_name = db.Column(db.String(255), nullable=False, unique=True)
    api_path = db.Column(db.String(255), nullable=False, unique=True)
    version = db.Column(db.String(50), default='1.0.0')
    description = db.Column(db.Text)
    input_schema = db.Column(db.Text)
    output_schema = db.Column(db.Text)
    swagger_spec = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')
    execution_count = db.Column(db.Integer, default=0)
    last_executed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'api_name': self.api_name,
            'api_path': self.api_path,
            'version': self.version,
            'description': self.description,
            'input_schema': json.loads(self.input_schema) if self.input_schema else {},
            'output_schema': json.loads(self.output_schema) if self.output_schema else {},
            'swagger_spec': json.loads(self.swagger_spec) if self.swagger_spec else {},
            'status': self.status,
            'execution_count': self.execution_count,
            'last_executed_at': self.last_executed_at.isoformat() if self.last_executed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
