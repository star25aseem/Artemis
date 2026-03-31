#!/bin/bash

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Checking Ollama..."

if ! command -v ollama &> /dev/null
then
    echo "❌ Ollama not installed."
    echo "👉 Install it from: https://ollama.com"
    exit 1
fi

echo "Pulling model..."
ollama pull llama3

echo "✅ Setup complete"