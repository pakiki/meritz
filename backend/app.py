from flask import Flask
from flask_cors import CORS
from database import init_db, db
from routes import workflow, application, engine
from routes.decision_tree import decision_tree_bp
from routes.scorecard import scorecard_bp
from routes.deployment import deployment_bp
from routes.dynamic_api import dynamic_api_bp
from routes.process_instance import process_instance_bp
from routes.human_task import human_task_bp
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    init_db(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(workflow.bp, url_prefix='/api/workflow')
    app.register_blueprint(application.bp, url_prefix='/api/application')
    app.register_blueprint(engine.bp, url_prefix='/api/engine')
    app.register_blueprint(decision_tree_bp, url_prefix='/api')
    app.register_blueprint(scorecard_bp, url_prefix='/api')
    app.register_blueprint(deployment_bp, url_prefix='/api')
    app.register_blueprint(dynamic_api_bp, url_prefix='/api')
    app.register_blueprint(process_instance_bp, url_prefix='/api')
    app.register_blueprint(human_task_bp, url_prefix='/api')
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'message': 'Flask server is running'}
    
    @app.route('/')
    def index():
        return {'message': 'Meritz Credit Evaluation BPM System API'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
