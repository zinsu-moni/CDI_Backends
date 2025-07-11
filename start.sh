#!/bin/bash
# Render startup script for Crop Disease Identification API

echo "🚀 Starting Crop Disease Identification API on Render..."

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Run diagnostics
echo "🔍 Running diagnostics..."
python diagnostic.py

if [ $? -eq 0 ]; then
    echo "✅ Diagnostics passed. Starting FastAPI application..."
    # Start the FastAPI application
    exec uvicorn main_fastapi:app --host 0.0.0.0 --port $PORT --workers 1 --timeout-keep-alive 30
else
    echo "❌ Diagnostics failed. Check logs for details."
    exit 1
fi
