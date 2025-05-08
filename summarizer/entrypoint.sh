#!/bin/bash
set -e

MODEL_DIR="/models"
MODEL_NAME="mistral-7b-instruct-v0.1.Q4_K_M.gguf"
HF_MODEL_ID="TheBloke/Mistral-7B-Instruct-v0.1-GGUF"

# Create model directory if it doesn't exist
mkdir -p "$MODEL_DIR"

# Download the model only if it's not already present
if [ ! -f "$MODEL_DIR/$MODEL_NAME" ]; then
    echo "📦 Downloading LLM model..."
    huggingface-cli download "$HF_MODEL_ID" "$MODEL_NAME" \
        --local-dir "$MODEL_DIR" \
        --local-dir-use-symlinks False
else
    echo "✅ LLM model already present."
fi

# Run the summarization script
echo "🚀 Starting summarizer..."
exec python summarize.py
