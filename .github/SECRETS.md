# GitHub Secrets Configuration

This document outlines the required secrets for the GitHub Actions workflow.

## Required Secrets

### Google Cloud Configuration
- `GOOGLE_SERVICE_ACCOUNT_KEY`: JSON key file for Google Cloud service account
- `GOOGLE_CLOUD_PROJECT`: Google Cloud project ID

## Setup Instructions

1. **Create a Google Cloud Service Account:**
   ```bash
   gcloud iam service-accounts create mlops-service-account \
     --display-name="MLOps Service Account"
   ```

2. **Grant necessary permissions:**
   ```bash
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:mlops-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/storage.admin"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:mlops-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/run.admin"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:mlops-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/aiplatform.user"
   ```

3. **Create and download the service account key:**
   ```bash
   gcloud iam service-accounts keys create credentials.json \
     --iam-account=mlops-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

4. **Add secrets to GitHub repository:**
   - Go to repository Settings > Secrets and variables > Actions
   - Add `GOOGLE_SERVICE_ACCOUNT_KEY` with the content of credentials.json
   - Add `GOOGLE_CLOUD_PROJECT` with your project ID

## Security Notes

- Never commit credentials.json to the repository
- Rotate service account keys regularly
- Use least privilege principle for service account permissions
- Monitor service account usage in Google Cloud Console