import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.app.extensions import db

def init_db():
    app = create_app()
    with app.app_context():
        print("Dropping all existing database tables...")
        db.drop_all()
        print("Creating all database tables...")
        db.create_all()
        print("Database tables initialized successfully!")

if __name__ == "__main__":
    init_db()
