from flask import Flask
from flask_cors import CORS
from database import init_db, db
from routes import workflow, application, engine
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    
    # CORS 설정 - React 앱과 통신
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 데이터베이스 초기화
    init_db(app)
    
    # 라우트 등록
    app.register_blueprint(workflow.bp, url_prefix='/api/workflow')
    app.register_blueprint(application.bp, url_prefix='/api/application')
    app.register_blueprint(engine.bp, url_prefix='/api/engine')
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'message': 'Flask server is running'}
    
    @app.route('/')
    def index():
        return {'message': 'Meritz Credit Evaluation Workflow System API'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
