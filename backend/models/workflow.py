from database import db
from datetime import datetime
import json

class Workflow(db.Model):
    """워크플로우 정의 모델"""
    __tablename__ = 'workflows'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    version = db.Column(db.String(50), default='1.0.0')
    status = db.Column(db.String(50), default='draft')  # draft, active, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    nodes = db.relationship('WorkflowNode', backref='workflow', lazy=True, cascade='all, delete-orphan')
    edges = db.relationship('WorkflowEdge', backref='workflow', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='workflow', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'nodes': [node.to_dict() for node in self.nodes],
            'edges': [edge.to_dict() for edge in self.edges]
        }

class WorkflowNode(db.Model):
    """워크플로우 노드 모델"""
    __tablename__ = 'workflow_nodes'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
    node_id = db.Column(db.String(100), nullable=False)  # 프론트엔드 노드 ID
    node_type = db.Column(db.String(50), nullable=False)  # start, end, decision, score, api
    label = db.Column(db.String(255))
    position_x = db.Column(db.Float, default=0)
    position_y = db.Column(db.Float, default=0)
    config = db.Column(db.Text)  # JSON 형태의 노드 설정
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'node_id': self.node_id,
            'node_type': self.node_type,
            'label': self.label,
            'position': {
                'x': self.position_x,
                'y': self.position_y
            },
            'config': json.loads(self.config) if self.config else {},
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class WorkflowEdge(db.Model):
    """워크플로우 엣지 (연결) 모델"""
    __tablename__ = 'workflow_edges'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
    edge_id = db.Column(db.String(100), nullable=False)  # 프론트엔드 엣지 ID
    source_node_id = db.Column(db.String(100), nullable=False)
    target_node_id = db.Column(db.String(100), nullable=False)
    source_handle = db.Column(db.String(50))
    target_handle = db.Column(db.String(50))
    label = db.Column(db.String(255))
    condition = db.Column(db.Text)  # 조건부 연결의 경우 조건식
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'edge_id': self.edge_id,
            'source': self.source_node_id,
            'target': self.target_node_id,
            'sourceHandle': self.source_handle,
            'targetHandle': self.target_handle,
            'label': self.label,
            'condition': self.condition,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
