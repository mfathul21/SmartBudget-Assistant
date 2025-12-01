#!/bin/bash

# Startup script for Render deployment

echo "🚀 Starting Financial Advisor..."

# Set Python path to include backend directory
export PYTHONPATH="${PYTHONPATH}:/opt/render/project/src/backend"

# Initialize database
echo "📦 Initializing database..."
cd backend
python -c "from database import init_db; init_db()"
echo "✅ Database initialized"

# Create admin user if not exists
echo "👤 Creating admin user..."
python init_admin.py || echo "⚠️ Admin user already exists or failed to create"

# Start Flask server with Gunicorn (production-ready)
echo "✅ Starting Flask server with Gunicorn..."
cd /opt/render/project/src
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile - wsgi:app
