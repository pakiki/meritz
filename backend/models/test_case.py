from datetime import datetime
from backend.database import db
import json


class TestCase(db.Model):
    __tablename__ = 'test_case'
    
    id = db.Column(db.Integer, primary_key=True)
    deployed_api_id = db.Column(db.Integer, db.ForeignKey('deployed_api.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    input_data = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    results = db.relationship('TestResult', backref='test_case', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'deployed_api_id': self.deployed_api_id,
            'name': self.name,
            'description': self.description,
            'input_data': json.loads(self.input_data) if self.input_data else {},
            'expected_output': json.loads(self.expected_output) if self.expected_output else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'results': [result.to_dict() for result in self.results]
        }


class TestResult(db.Model):
    __tablename__ = 'test_result'
    
    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_case.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    actual_output = db.Column(db.Text)
    error_message = db.Column(db.Text)
    execution_time_ms = db.Column(db.Integer)
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'test_case_id': self.test_case_id,
            'status': self.status,
            'actual_output': json.loads(self.actual_output) if self.actual_output else {},
            'error_message': self.error_message,
            'execution_time_ms': self.execution_time_ms,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None
        }
