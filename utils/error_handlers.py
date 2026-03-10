# utils/error_handlers.py
from flask import jsonify
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError
from werkzeug.exceptions import HTTPException
import traceback
from extensions import db

def register_error_handlers(app):
    """Register error handlers for the app"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors"""
        app.logger.warning(f'Bad request: {str(error)}')
        return jsonify({
            'error': 'Bad Request',
            'message': str(error) or 'The request was invalid'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle unauthorized access errors"""
        app.logger.warning(f'Unauthorized access attempt: {str(error)}')
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Please log in to access this resource'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle forbidden access errors"""
        app.logger.warning(f'Forbidden access attempt: {str(error)}')
        return jsonify({
            'error': 'Forbidden',
            'message': 'You don\'t have permission to access this resource'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle resource not found errors"""
        app.logger.info(f'Resource not found: {str(error)}')
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle method not allowed errors"""
        app.logger.warning(f'Method not allowed: {str(error)}')
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for this endpoint'
        }), 405
    
    @app.errorhandler(409)
    def conflict(error):
        """Handle conflict errors (e.g., duplicate entries)"""
        app.logger.warning(f'Conflict: {str(error)}')
        return jsonify({
            'error': 'Conflict',
            'message': str(error) or 'Resource already exists'
        }), 409
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Handle validation errors"""
        app.logger.warning(f'Validation error: {str(error)}')
        return jsonify({
            'error': 'Validation Error',
            'message': str(error) or 'The request could not be processed',
            'details': getattr(error, 'data', {}).get('messages', {})
        }), 422
    
    @app.errorhandler(429)
    def too_many_requests(error):
        """Handle rate limit errors"""
        app.logger.warning(f'Rate limit exceeded: {str(error)}')
        return jsonify({
            'error': 'Too Many Requests',
            'message': 'You have exceeded the rate limit. Please try again later.'
        }), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle internal server errors"""
        app.logger.error(f'Internal server error: {str(error)}')
        app.logger.error(traceback.format_exc())
        
        # Rollback database session if there's an active transaction
        try:
            db.session.rollback()
        except:
            pass
        
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Something went wrong on our end. Please try again later.'
        }), 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle service unavailable errors"""
        app.logger.error(f'Service unavailable: {str(error)}')
        return jsonify({
            'error': 'Service Unavailable',
            'message': 'The service is temporarily unavailable. Please try again later.'
        }), 503
    
    # JWT specific errors
    @app.errorhandler(PyJWTError)
    def handle_jwt_error(error):
        """Handle JWT token errors"""
        app.logger.warning(f'JWT error: {str(error)}')
        return jsonify({
            'error': 'Authentication Error',
            'message': 'Your authentication token is invalid or expired. Please log in again.'
        }), 401
    
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_extended_error(error):
        """Handle Flask-JWT-Extended specific errors"""
        app.logger.warning(f'JWT Extended error: {str(error)}')
        return jsonify({
            'error': 'Authentication Error',
            'message': str(error) or 'There was an error with your authentication.'
        }), 401
    
    # Handle all other exceptions
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle any unexpected errors"""
        app.logger.error(f'Unexpected error: {str(error)}')
        app.logger.error(traceback.format_exc())
        
        # Rollback database session if there's an active transaction
        try:
            db.session.rollback()
        except:
            pass
        
        # Don't expose internal error details in production
        if app.config.get('DEBUG', False):
            message = str(error)
        else:
            message = 'An unexpected error occurred. Please try again later.'
        
        return jsonify({
            'error': 'Unexpected Error',
            'message': message
        }), 500