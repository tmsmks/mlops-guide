# MLOps Project - Cloud Deployment

This is a comprehensive machine learning operations project that demonstrates end-to-end MLOps practices with cloud deployment, including data versioning, experiment tracking, model serving, and monitoring.

## 🏗️ Project Structure

- `src/` - Source code for the ML pipeline
  - `prepare.py` - Data preprocessing and preparation
  - `train.py` - Model training with MLflow tracking
  - `evaluate.py` - Model evaluation and metrics generation
  - `serve.py` - FastAPI model serving service
  - `monitor.py` - Model monitoring and drift detection
  - `utils/` - Utility functions
- `data/` - Data storage (raw and prepared datasets)
- `model/` - Trained model artifacts
- `evaluation/` - Model evaluation results and plots
- `monitoring/` - Model monitoring reports
- `params.yaml` - Experiment parameters
- `dvc.yaml` - DVC pipeline configuration
- `mlflow_config.py` - MLflow configuration for cloud deployment
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Local development setup
- `deploy.sh` - Google Cloud deployment script

## 🚀 Features

### Data Management
- **DVC Integration**: Version control for datasets with Google Cloud Storage backend
- **Data Pipeline**: Automated data preprocessing and preparation

### Experiment Tracking
- **MLflow Integration**: Comprehensive experiment tracking and model registry
- **Cloud Storage**: All experiments and models stored in Google Cloud Storage
- **Model Versioning**: Automatic model versioning and registry management

### Model Serving
- **FastAPI Service**: RESTful API for model inference
- **Docker Containerization**: Containerized deployment for scalability
- **Cloud Run Deployment**: Serverless deployment on Google Cloud Run

### Monitoring & Observability
- **Performance Monitoring**: Automated model performance tracking
- **Drift Detection**: Data and concept drift detection
- **Health Checks**: Service health monitoring endpoints

### CI/CD Pipeline
- **GitHub Actions**: Automated training, testing, and deployment
- **Cloud Integration**: Seamless Google Cloud Platform integration
- **Automated Reports**: CML-generated performance reports

## 🛠️ Setup

### Prerequisites
- Python 3.12+
- Docker
- Google Cloud SDK
- DVC
- MLflow

### Local Development

1. **Clone and setup environment:**
   ```bash
   git clone <repository-url>
   cd mlops-project
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Cloud:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

4. **Setup DVC remote:**
   ```bash
   dvc remote add -d storage gs://your-bucket-name
   ```

5. **Run the pipeline:**
   ```bash
   dvc repro
   ```

### Docker Development

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access services:**
   - Model API: http://localhost:8000
   - MLflow UI: http://localhost:5000

## 🔧 Usage

### Training Models
```bash
# Run full pipeline
dvc repro

# Train with specific parameters
python src/train.py data/prepared model
```

### Model Serving
```bash
# Start the service
python src/serve.py

# Or with Docker
docker run -p 8000:8000 mlops-service
```

### Monitoring
```bash
# Generate monitoring report
python src/monitor.py

# Check service health
curl http://localhost:8000/health
```

### API Usage
```bash
# Make predictions
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": [0.1, 0.2, ...],
    "image_shape": [32, 32, 1]
  }'
```

## ☁️ Cloud Deployment

### Google Cloud Run Deployment
```bash
# Deploy to Google Cloud Run
./deploy.sh
```

### Manual Deployment
```bash
# Build and push image
docker build -t gcr.io/PROJECT_ID/mlops-service .
docker push gcr.io/PROJECT_ID/mlops-service

# Deploy to Cloud Run
gcloud run deploy mlops-service \
  --image gcr.io/PROJECT_ID/mlops-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📊 Monitoring & Observability

### MLflow Tracking
- **Experiment Tracking**: All experiments logged to MLflow
- **Model Registry**: Centralized model versioning and management
- **Artifact Storage**: Models and artifacts stored in Google Cloud Storage

### Performance Monitoring
- **Automated Reports**: Daily performance monitoring reports
- **Drift Detection**: Automatic detection of model performance degradation
- **Alerting**: Configurable alerts for performance issues

### Service Monitoring
- **Health Endpoints**: `/health` and `/` for service status
- **Metrics**: Request latency, throughput, and error rates
- **Logging**: Comprehensive logging for debugging and analysis

## 🔄 Pipeline Stages

1. **Prepare** - Data preprocessing and preparation with DVC tracking
2. **Train** - Model training with MLflow experiment tracking
3. **Evaluate** - Model evaluation and metrics generation
4. **Monitor** - Performance monitoring and drift detection
5. **Deploy** - Automated deployment to Google Cloud Run
6. **Serve** - Model serving via FastAPI

## 📈 CI/CD Pipeline

The GitHub Actions workflow automatically:
- Trains models on code changes
- Runs evaluation and monitoring
- Builds and deploys Docker containers
- Generates performance reports
- Updates model registry

## 🛡️ Security & Best Practices

- **Environment Variables**: Sensitive configuration via environment variables
- **Service Accounts**: Google Cloud authentication via service accounts
- **Container Security**: Multi-stage Docker builds for minimal attack surface
- **API Security**: Input validation and error handling
- **Monitoring**: Comprehensive logging and monitoring

## 📚 Documentation

- **API Documentation**: Available at `/docs` when service is running
- **MLflow UI**: Experiment tracking and model registry interface
- **Monitoring Reports**: Generated in `monitoring/` directory
- **DVC Pipeline**: Visualized with `dvc dag` command