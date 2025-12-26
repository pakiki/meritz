import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Flask 애플리케이션 설정"""
    
    # Flask 설정
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # 데이터베이스 설정
    DATABASE_PATH = os.environ.get(
        'DATABASE_PATH',
        str(BASE_DIR / 'database' / 'meritz.db')
    )
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API 설정
    JSON_SORT_KEYS = False
    JSON_AS_ASCII = False
    
    # 페이지네이션
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """프로덕션 환경 설정"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """테스트 환경 설정"""
    DEBUG = True
    TESTING = True
    DATABASE_PATH = ':memory:'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
