#!/bin/bash
# Render startup script for Crop Disease Identification API

echo "🚀 Starting Crop Disease Identification API on Render..."

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Start the FastAPI application
uvicorn main_fastapi:app --host 0.0.0.0 --port $PORT --workers 1
