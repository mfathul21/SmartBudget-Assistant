from config import FLASK_CONFIG
from flask import Flask
from database import get_db

app = Flask(__name__)
app.config.update(FLASK_CONFIG)

with app.app_context():
    db = get_db()
    cur = db.execute("SELECT id, name, role, ocr_enabled FROM users WHERE id=1")
    r = cur.fetchone()
    if r:
        print(f"User ID 1: {r['name']} ({r['role']})")
        print(f"OCR Enabled DB value: {r['ocr_enabled']}")
        print(f"Type: {type(r['ocr_enabled']).__name__}")
        print(f"Boolean cast: {bool(r['ocr_enabled'])}")
    else:
        print("User ID 1 tidak ditemukan")
