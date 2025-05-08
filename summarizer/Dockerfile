FROM python:3.11-slim

# Install build dependencies and OpenBLAS for llama-cpp
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install llama-cpp-python
RUN pip install llama-cpp-python

# Copy model and script
WORKDIR /app
COPY summarize.py .
COPY models /models

CMD ["python", "summarize.py"]
