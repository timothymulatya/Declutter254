from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Import models
    from models import User, Category, Item, Request
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.category_routes import category_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    
    # Test route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Declutter254 API is running!',
            'status': 'success',
            'version': '1.0',
            'endpoints': {
                'auth': '/api/auth/register, /api/auth/login, /api/auth/profile',
                'categories': '/api/categories/'
            }
        })
    
    @app.route('/health')
    def health_check():
        try:
            db.session.execute('SELECT 1')
            db_status = 'connected'
        except Exception as e:
            db_status = 'error'
        
        return jsonify({
            'api': 'running',
            'database': db_status,
            'environment': 'development'
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5555)