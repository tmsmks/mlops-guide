FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY params.yaml .

# Set environment variables
ENV PYTHONPATH=/app
ENV MLFLOW_TRACKING_URI=gs://mlops-project-storage/mlflow
ENV MLFLOW_EXPERIMENT_NAME=mlops-experiment

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "src/serve.py"]