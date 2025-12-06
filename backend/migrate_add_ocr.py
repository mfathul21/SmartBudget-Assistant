"""
Database migration script to add OCR feature toggle
Run this script to update existing database with ocr_enabled column
"""

import sqlite3
from pathlib import Path

# Get database path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "backend" / "finance.db"


def migrate_add_ocr_enabled():
    """Add ocr_enabled column to users table"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]

        if "ocr_enabled" not in columns:
            print("Adding ocr_enabled column to users table...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN ocr_enabled BOOLEAN DEFAULT FALSE
            """)
            conn.commit()
            print("✅ Migration successful: ocr_enabled column added")
        else:
            print("ℹ️  Column ocr_enabled already exists, skipping migration")

        conn.close()

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise


if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration: Add OCR Feature Toggle")
    print("=" * 60)
    migrate_add_ocr_enabled()
    print("=" * 60)
