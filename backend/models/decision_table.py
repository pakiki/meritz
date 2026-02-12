from datetime import datetime
from backend.database import db
import json


class DecisionTable(db.Model):
    __tablename__ = 'decision_table'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    hit_policy = db.Column(db.String(50), default='FIRST')
    conditions = db.Column(db.Text)
    actions = db.Column(db.Text)
    status = db.Column(db.String(50), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    rules = db.relationship('DecisionTableRule', backref='table', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'hit_policy': self.hit_policy,
            'conditions': json.loads(self.conditions) if self.conditions else [],
            'actions': json.loads(self.actions) if self.actions else [],
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'rules': [rule.to_dict() for rule in self.rules]
        }


class DecisionTableRule(db.Model):
    __tablename__ = 'decision_table_rule'
    
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('decision_table.id'), nullable=False)
    rule_number = db.Column(db.Integer, nullable=False)
    conditions = db.Column(db.Text)
    actions = db.Column(db.Text)
    priority = db.Column(db.Integer, default=0)
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'table_id': self.table_id,
            'rule_number': self.rule_number,
            'conditions': json.loads(self.conditions) if self.conditions else {},
            'actions': json.loads(self.actions) if self.actions else {},
            'priority': self.priority,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
