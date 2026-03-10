import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # Secret key for sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Token expires in 24 hours
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///declutter.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False