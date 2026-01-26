FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY pyproject.toml .
COPY rag/ ./rag/
COPY app.py .

# Install dependencies
RUN pip install --no-cache-dir \
    streamlit>=1.40.0 \
    google-cloud-aiplatform[adk,agent-engines]>=1.108.0 \
    google-adk>=1.10.0 \
    python-dotenv \
    google-auth \
    arize-otel>=0.8.2 \
    openinference-instrumentation-google-adk>=0.1.0 \
    openinference-instrumentation>=0.1.34 \
    arize>=7.36.0

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080

# Run Streamlit
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
