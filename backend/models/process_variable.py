from datetime import datetime
from backend.database import db
import json


class ProcessVariable(db.Model):
    __tablename__ = 'process_variable'
    
    id = db.Column(db.Integer, primary_key=True)
    process_instance_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Text)
    value_type = db.Column(db.String(50), default='STRING')
    scope = db.Column(db.String(50), default='PROCESS')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        value_data = self.value
        if self.value_type == 'JSON' and value_data:
            try:
                value_data = json.loads(value_data)
            except:
                pass
        elif self.value_type == 'INTEGER' and value_data:
            value_data = int(value_data)
        elif self.value_type == 'FLOAT' and value_data:
            value_data = float(value_data)
        elif self.value_type == 'BOOLEAN' and value_data:
            value_data = value_data.lower() == 'true'
            
        return {
            'id': self.id,
            'process_instance_id': self.process_instance_id,
            'name': self.name,
            'value': value_data,
            'value_type': self.value_type,
            'scope': self.scope,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
