#!/bin/bash
# Render build script

echo "🔨 Building Crop Disease Identification API..."

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads

echo "✅ Build completed successfully!"
