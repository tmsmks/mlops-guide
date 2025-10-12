#!/bin/bash

# Deploy script for Google Cloud Run
set -e

# Configuration
PROJECT_ID="mlops-project-$(date +%s)"
REGION="us-central1"
SERVICE_NAME="mlops-model-service"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "Deploying MLOps service to Google Cloud Run..."

# Set project
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable aiplatform.googleapis.com

# Create bucket for DVC and MLflow
gsutil mb gs://mlops-project-storage || echo "Bucket already exists"

# Build and push Docker image
gcloud builds submit --tag $IMAGE_NAME .

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --set-env-vars MLFLOW_TRACKING_URI=gs://mlops-project-storage/mlflow,MLFLOW_EXPERIMENT_NAME=mlops-experiment

echo "Deployment complete!"
echo "Service URL: https://$SERVICE_NAME-$REGION-$PROJECT_ID.a.run.app"