"""Initialize database and create admin user"""

from flask import Flask
from database import init_db

app = Flask(__name__)

with app.app_context():
    init_db()
    print("\n✅ Database initialized successfully!")
    print("👤 Admin login:")
    print("   Email: muhammadfathul386@gmail.com")
    print("   Password: cuwiklucu08")
