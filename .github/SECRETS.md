# GitHub Secrets Configuration

## ⚠️ IMPORTANT: Required Setup

The GitHub Actions workflow **WILL FAIL** without these secrets configured.

## 🔐 Required Secrets

### 1. GOOGLE_SERVICE_ACCOUNT_KEY
- **Type**: Repository Secret
- **Value**: Complete JSON content of service account key file
- **Format**: `{"type": "service_account", "project_id": "...", ...}`

### 2. GOOGLE_CLOUD_PROJECT  
- **Type**: Repository Secret
- **Value**: Your Google Cloud project ID
- **Format**: `my-mlops-project-123456`

## 🚀 Quick Setup

### Step 1: Create Service Account
```bash
# Replace YOUR_PROJECT_ID with your actual project ID
export PROJECT_ID="YOUR_PROJECT_ID"

# Create service account
gcloud iam service-accounts create mlops-service-account \
  --display-name="MLOps Service Account" \
  --project=$PROJECT_ID

# Grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:mlops-service-account@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:mlops-service-account@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:mlops-service-account@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:mlops-service-account@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.builder"

# Create key file
gcloud iam service-accounts keys create credentials.json \
  --iam-account=mlops-service-account@$PROJECT_ID.iam.gserviceaccount.com \
  --project=$PROJECT_ID
```

### Step 2: Create Storage Bucket
```bash
# Create bucket for DVC and MLflow
gsutil mb gs://mlops-project-storage
```

### Step 3: Add GitHub Secrets
1. Go to: `https://github.com/tmsmks/mlops-guide/settings/secrets/actions`
2. Click **"New repository secret"**
3. Add these two secrets:

**Secret 1:**
- Name: `GOOGLE_SERVICE_ACCOUNT_KEY`
- Value: Copy entire content of `credentials.json`

**Secret 2:**
- Name: `GOOGLE_CLOUD_PROJECT`  
- Value: Your project ID (e.g., `my-mlops-project-123456`)

## ✅ Verification

After adding secrets, the workflow will:
1. ✅ Validate secrets are configured
2. ✅ Build and test the application
3. ✅ Deploy to Google Cloud Run
4. ✅ Generate monitoring reports

## 🚨 Common Issues

- **"GOOGLE_CLOUD_PROJECT secret is not set"** → Add the secret in GitHub
- **"Authentication failed"** → Check service account key is valid JSON
- **"Bucket not found"** → Create `gs://mlops-project-storage` bucket
- **"Permission denied"** → Verify service account has required roles

## 📖 Detailed Instructions

See `GITHUB_SETUP.md` for complete step-by-step instructions.