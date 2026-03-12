# config.py - CLEAN MVP VERSION
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # Secret keys
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///declutter.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
   
    ITEMS_PER_PAGE = 20