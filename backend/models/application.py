from database import db
from datetime import datetime
import json

class Application(db.Model):
    """신청서 모델"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
    applicant_name = db.Column(db.String(255))
    applicant_id = db.Column(db.String(100))  # 주민등록번호 또는 식별자
    application_data = db.Column(db.Text)  # JSON 형태의 신청 데이터
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, rejected
    score = db.Column(db.Float)
    result = db.Column(db.Text)  # JSON 형태의 평가 결과
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # 관계
    logs = db.relationship('ApplicationLog', backref='application', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'applicant_name': self.applicant_name,
            'applicant_id': self.applicant_id,
            'application_data': json.loads(self.application_data) if self.application_data else {},
            'status': self.status,
            'score': self.score,
            'result': json.loads(self.result) if self.result else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class ApplicationLog(db.Model):
    """신청서 실행 로그 모델"""
    __tablename__ = 'application_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    node_id = db.Column(db.String(100))
    node_type = db.Column(db.String(50))
    action = db.Column(db.String(100))
    input_data = db.Column(db.Text)  # JSON 형태
    output_data = db.Column(db.Text)  # JSON 형태
    status = db.Column(db.String(50))  # success, error, skipped
    error_message = db.Column(db.Text)
    execution_time = db.Column(db.Float)  # 실행 시간 (초)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'node_id': self.node_id,
            'node_type': self.node_type,
            'action': self.action,
            'input_data': json.loads(self.input_data) if self.input_data else {},
            'output_data': json.loads(self.output_data) if self.output_data else {},
            'status': self.status,
            'error_message': self.error_message,
            'execution_time': self.execution_time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
