# Use the official Python image as a base
FROM python:3.11-slim

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0:11434
ENV STREAMLIT_PORT=8501

# Set the working directory
WORKDIR /app
# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

RUN ollama serve & \
    sleep 5 && \
    ollama pull llama3
# Install Python dependencies
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports for Ollama and Streamlit
EXPOSE 11434 8501

# Start both Ollama and the Streamlit application
CMD streamlit run app.py
