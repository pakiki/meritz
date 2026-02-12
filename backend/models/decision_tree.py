from datetime import datetime
from backend.database import db
import json


class DecisionTree(db.Model):
    __tablename__ = 'decision_tree'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    target_variable = db.Column(db.String(100), nullable=False)
    algorithm = db.Column(db.String(50), default='gini')
    max_depth = db.Column(db.Integer, default=5)
    min_samples_split = db.Column(db.Integer, default=2)
    min_samples_leaf = db.Column(db.Integer, default=1)
    status = db.Column(db.String(50), default='draft')
    training_accuracy = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    nodes = db.relationship('DecisionTreeNode', backref='tree', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'target_variable': self.target_variable,
            'algorithm': self.algorithm,
            'max_depth': self.max_depth,
            'min_samples_split': self.min_samples_split,
            'min_samples_leaf': self.min_samples_leaf,
            'status': self.status,
            'training_accuracy': self.training_accuracy,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'nodes': [node.to_dict() for node in self.nodes]
        }


class DecisionTreeNode(db.Model):
    __tablename__ = 'decision_tree_node'
    
    id = db.Column(db.Integer, primary_key=True)
    tree_id = db.Column(db.Integer, db.ForeignKey('decision_tree.id'), nullable=False)
    node_id = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.String(50))
    feature = db.Column(db.String(100))
    threshold = db.Column(db.Float)
    operator = db.Column(db.String(20))
    is_leaf = db.Column(db.Boolean, default=False)
    class_label = db.Column(db.String(100))
    samples = db.Column(db.Integer)
    gini = db.Column(db.Float)
    entropy = db.Column(db.Float)
    value = db.Column(db.Text)
    position_x = db.Column(db.Float)
    position_y = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tree_id': self.tree_id,
            'node_id': self.node_id,
            'parent_id': self.parent_id,
            'feature': self.feature,
            'threshold': self.threshold,
            'operator': self.operator,
            'is_leaf': self.is_leaf,
            'class_label': self.class_label,
            'samples': self.samples,
            'gini': self.gini,
            'entropy': self.entropy,
            'value': json.loads(self.value) if self.value else None,
            'position_x': self.position_x,
            'position_y': self.position_y,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
