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

# Copy project files
COPY summarize.py .
COPY entrypoint.sh .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
