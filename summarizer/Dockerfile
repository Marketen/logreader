FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages and Hugging Face CLI
RUN pip install --no-binary llama-cpp-python --force-reinstall llama-cpp-python \
    huggingface_hub

# Set environment variables
ENV CMAKE_ARGS="-DLLAMA_MAX_CONTEXT=4096"

# Set working directory
WORKDIR /app

# Download the model using Hugging Face CLI
RUN huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.1-GGUF \
    mistral-7b-instruct-v0.1.Q4_K_M.gguf \
    --local-dir /models \
    --local-dir-use-symlinks False

# Copy your script into the container
COPY summarize.py .

# Default command
CMD ["python", "summarize.py"]
