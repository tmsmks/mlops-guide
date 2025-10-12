#!/bin/bash

# Google Cloud Setup Script for MLOps Project
# Project ID: machledata-474307

set -e

PROJECT_ID="machledata-474307"
SERVICE_ACCOUNT_NAME="mlops-service-account"
BUCKET_NAME="mlops-project-storage"

echo "🚀 Setting up Google Cloud for MLOps project..."
echo "Project ID: $PROJECT_ID"

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "📋 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Create service account
echo "👤 Creating service account..."
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
  --display-name="MLOps Service Account" \
  --description="Service account for MLOps CI/CD pipeline" \
  --project=$PROJECT_ID || echo "Service account may already exist"

# Grant necessary permissions
echo "🔐 Granting permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.builder"

# Create storage bucket
echo "🪣 Creating storage bucket..."
gsutil mb gs://$BUCKET_NAME || echo "Bucket may already exist"

# Create service account key
echo "🔑 Creating service account key..."
gcloud iam service-accounts keys create credentials.json \
  --iam-account=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com \
  --project=$PROJECT_ID

echo "✅ Google Cloud setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Add the following secrets to GitHub:"
echo "   - GOOGLE_SERVICE_ACCOUNT_KEY: Content of credentials.json"
echo "   - GOOGLE_CLOUD_PROJECT: $PROJECT_ID"
echo ""
echo "2. GitHub secrets URL:"
echo "   https://github.com/tmsmks/mlops-guide/settings/secrets/actions"
echo ""
echo "3. Test the setup:"
echo "   python validate_setup.py"