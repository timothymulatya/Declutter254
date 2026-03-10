# app.py
from flask import Flask, jsonify
from extensions import db, migrate, cors, bcrypt, jwt
from config import Config
from utils.error_handlers import register_error_handlers
from utils.logger import setup_logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Setup logging
    setup_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Import models
    with app.app_context():
        from models import User, Category, Item, Request
    
    # Import and register blueprints
    from routes.auth_routes import auth_bp
    from routes.category_routes import category_bp
    from routes.item_routes import item_bp
    from routes.request_routes import request_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(request_bp)
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Declutter254 API is running!',
            'status': 'success',
            'version': '1.0',
            'endpoints': {
                'auth': '/api/auth/register, /api/auth/login, /api/auth/profile',
                'categories': '/api/categories/',
                'items': '/api/items/ (GET, POST), /api/items/<id> (GET, PUT, DELETE)',
                'requests': '/api/requests/incoming, /api/requests/outgoing, /api/requests/item/<id>'
            }
        })
    
    # Health check route
    @app.route('/health')
    def health_check():
        try:
            db.session.execute('SELECT 1')
            db_status = 'connected'
        except Exception as e:
            db_status = f'error: {str(e)}'
            app.logger.error(f'Database health check failed: {str(e)}')
        
        return jsonify({
            'api': 'running',
            'database': db_status,
            'environment': app.config.get('ENV', 'development')
        })
    
    # Log application startup
    app.logger.info('Declutter254 application started successfully')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5555)