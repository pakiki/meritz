from datetime import datetime
from backend.database import db
import json


class Scorecard(db.Model):
    __tablename__ = 'scorecard'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    base_score = db.Column(db.Float, default=600)
    pdo = db.Column(db.Float, default=20)
    base_odds = db.Column(db.Float, default=50)
    status = db.Column(db.String(50), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    characteristics = db.relationship('ScorecardCharacteristic', backref='scorecard', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'base_score': self.base_score,
            'pdo': self.pdo,
            'base_odds': self.base_odds,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'characteristics': [char.to_dict() for char in self.characteristics]
        }


class ScorecardCharacteristic(db.Model):
    __tablename__ = 'scorecard_characteristic'
    
    id = db.Column(db.Integer, primary_key=True)
    scorecard_id = db.Column(db.Integer, db.ForeignKey('scorecard.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    attributes = db.relationship('ScorecardAttribute', backref='characteristic', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'scorecard_id': self.scorecard_id,
            'name': self.name,
            'weight': self.weight,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'attributes': [attr.to_dict() for attr in self.attributes]
        }


class ScorecardAttribute(db.Model):
    __tablename__ = 'scorecard_attribute'
    
    id = db.Column(db.Integer, primary_key=True)
    characteristic_id = db.Column(db.Integer, db.ForeignKey('scorecard_characteristic.id'), nullable=False)
    attribute = db.Column(db.String(255), nullable=False)
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    category = db.Column(db.String(100))
    good_count = db.Column(db.Integer, default=0)
    bad_count = db.Column(db.Integer, default=0)
    woe = db.Column(db.Float)
    iv = db.Column(db.Float)
    points = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'characteristic_id': self.characteristic_id,
            'attribute': self.attribute,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'category': self.category,
            'good_count': self.good_count,
            'bad_count': self.bad_count,
            'woe': self.woe,
            'iv': self.iv,
            'points': self.points,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
