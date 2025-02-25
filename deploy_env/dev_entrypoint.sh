#!/bin/sh
set -e 


echo "Starting FastAPI..."
exec uvicorn foodshareapp.app.application:app --host 0.0.0.0 --port 8000 --reload
