from database import get_db
from config import FLASK_CONFIG
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

app = Flask(__name__)
app.config.update(FLASK_CONFIG)
db = SQLAlchemy(app)

with app.app_context():
    inspector = inspect(db.engine)
    
    if 'users' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('users')]
        print('Users table columns:', columns)
        print('Has ocr_enabled:', 'ocr_enabled' in columns)
        print('Has image_urls:', 'image_urls' in columns)
    else:
        print('ERROR: users table not found!')
