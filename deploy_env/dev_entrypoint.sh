#!/bin/sh
set -e 

echo "Applying database migrations..."
alembic upgrade head

echo "Loading sample data..."
python deploy_env/load_sample_data.py

echo "Starting FastAPI..."
exec uvicorn foodshareapp.app.application:app --host 0.0.0.0 --port 8000 --reload
