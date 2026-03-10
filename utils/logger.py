import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """Setup logging configuration for the application"""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
        print("📁 Created logs directory")
    
    # File handler for all logs and rotating to prevent huge files
    file_handler = RotatingFileHandler(
        'logs/declutter254.log', 
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Console handler for errors (prints to terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    console_handler.setLevel(logging.ERROR)
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    # Log startup message
    app.logger.info('=' * 50)
    app.logger.info('Declutter254 Application Starting')
    app.logger.info('=' * 50)
    app.logger.info(f'Environment: {app.config.get("ENV", "development")}')
    app.logger.info(f'Debug mode: {app.config.get("DEBUG", False)}')
    app.logger.info(f'Database: {app.config.get("SQLALCHEMY_DATABASE_URI")}')
    
    return app.logger