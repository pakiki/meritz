from database import db
from datetime import datetime
import json

class Rule(db.Model):
    """평가 규칙 모델"""
    __tablename__ = 'rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    rule_type = db.Column(db.String(50), nullable=False)  # score, decision, validation
    category = db.Column(db.String(100))  # 소득, 신용, 부채 등
    condition = db.Column(db.Text)  # 규칙 조건식
    action = db.Column(db.Text)  # 규칙 액션 (JSON)
    priority = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rule_type': self.rule_type,
            'category': self.category,
            'condition': self.condition,
            'action': json.loads(self.action) if self.action else {},
            'priority': self.priority,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
