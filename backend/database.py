from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    """데이터베이스 초기화"""
    db.init_app(app)
    
    with app.app_context():
        # 데이터베이스 파일 디렉토리 생성
        db_path = app.config['DATABASE_PATH']
        if db_path != ':memory:':
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # 테이블 생성
        db.create_all()
        
        print(f"Database initialized at: {db_path}")

def get_db():
    """데이터베이스 인스턴스 반환"""
    return db
