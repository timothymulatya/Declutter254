# utils/error_handlers.py
from flask import jsonify
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError

def register_error_handlers(app):
    """Register error handlers for the app"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized', 'message': 'Please log in to access this resource'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden', 'message': 'You don\'t have permission to access this resource'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': 'The requested resource was not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error', 'message': 'Something went wrong on our end'}), 500
    
    # JWT specific errors
    @app.errorhandler(PyJWTError)
    def jwt_error(error):
        return jsonify({'error': 'Invalid token', 'message': 'Your authentication token is invalid or expired'}), 401