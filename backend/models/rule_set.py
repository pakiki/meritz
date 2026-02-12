from datetime import datetime
from backend.database import db
import json


class RuleSet(db.Model):
    __tablename__ = 'rule_set'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    rule_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    rules = db.relationship('Rule', backref='rule_set', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rule_type': self.rule_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'rules': [rule.to_dict() for rule in self.rules]
        }


class Rule(db.Model):
    __tablename__ = 'rule'
    
    id = db.Column(db.Integer, primary_key=True)
    rule_set_id = db.Column(db.Integer, db.ForeignKey('rule_set.id'))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    condition = db.Column(db.Text, nullable=False)
    action = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, default=0)
    enabled = db.Column(db.Boolean, default=True)
    metadata = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'rule_set_id': self.rule_set_id,
            'name': self.name,
            'description': self.description,
            'condition': self.condition,
            'action': self.action,
            'priority': self.priority,
            'enabled': self.enabled,
            'metadata': json.loads(self.metadata) if self.metadata else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
