import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app

app = create_app()

# This is required for Vercel
app.debug = False
