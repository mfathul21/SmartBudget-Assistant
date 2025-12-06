from config import FLASK_CONFIG
from flask import Flask
from database import get_db
import json

app = Flask(__name__)
app.config.update(FLASK_CONFIG)

with app.app_context():
    db = get_db()
    cur = db.execute(
        "SELECT id, name, email, role, created_at, ocr_enabled FROM users ORDER BY created_at DESC"
    )
    
    # Ini adalah kode yang SAMA PERSIS dengan backend/main.py line 1193-1203
    rows = [
        {
            "id": r["id"],
            "name": r["name"],
            "email": r["email"],
            "role": r["role"],
            "created_at": r["created_at"],
            "ocr_enabled": bool(r.get("ocr_enabled", False)),
        }
        for r in cur.fetchall()
    ]
    
    print("\n" + "="*80)
    print("SIMULASI API RESPONSE /api/admin/users (GET)")
    print("="*80)
    print(json.dumps(rows, indent=2, default=str))
    print("\n" + "="*80)
    print("DETAIL PER USER:")
    print("="*80)
    for u in rows:
        print(f"ID: {u['id']} | {u['name']:25s} | OCR: {u['ocr_enabled']} (type: {type(u['ocr_enabled']).__name__})")
