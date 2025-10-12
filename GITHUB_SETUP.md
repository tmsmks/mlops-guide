# GitHub Secrets Configuration

## 🔐 Required Secrets

To make the GitHub Actions workflow work, you need to configure the following secrets in your GitHub repository:

### 1. GOOGLE_SERVICE_ACCOUNT_KEY
- **Description**: JSON key file for Google Cloud service account
- **How to get it**:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Navigate to IAM & Admin > Service Accounts
  3. Create a new service account or use existing one
  4. Create a JSON key and download it
  5. Copy the entire JSON content

### 2. GOOGLE_CLOUD_PROJECT
- **Description**: Your Google Cloud project ID
- **How to get it**:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Select your project
  3. Copy the Project ID from the project info panel

## 📋 Step-by-Step Setup

### Step 1: Create Google Cloud Service Account

```bash
# Create service account
gcloud iam service-accounts create mlops-service-account \
  --display-name="MLOps Service Account" \
  --description="Service account for MLOps CI/CD pipeline"

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:mlops-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:mlops-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:mlops-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:mlops-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.builder"

# Create and download key
gcloud iam service-accounts keys create credentials.json \
  --iam-account=mlops-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### Step 2: Create Google Cloud Storage Bucket

```bash
# Create bucket for DVC and MLflow
gsutil mb gs://mlops-project-storage

# Make bucket publicly readable (optional, for MLflow UI)
gsutil iam ch allUsers:objectViewer gs://mlops-project-storage
```

### Step 3: Configure GitHub Secrets

1. Go to your GitHub repository: `https://github.com/tmsmks/mlops-guide`
2. Click on **Settings** tab
3. In the left sidebar, click on **Secrets and variables** > **Actions**
4. Click **New repository secret**
5. Add the following secrets:

#### Secret 1: GOOGLE_SERVICE_ACCOUNT_KEY
- **Name**: `GOOGLE_SERVICE_ACCOUNT_KEY`
- **Value**: Paste the entire content of the `credentials.json` file

#### Secret 2: GOOGLE_CLOUD_PROJECT
- **Name**: `GOOGLE_CLOUD_PROJECT`
- **Value**: Your Google Cloud project ID (e.g., `my-mlops-project-123456`)

### Step 4: Enable Required APIs

```bash
# Enable required Google Cloud APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

## ✅ Verification

After setting up the secrets, you can verify the configuration by:

1. **Check secrets are set**: Go to repository Settings > Secrets and variables > Actions
2. **Run the workflow**: Push a commit or manually trigger the workflow
3. **Check logs**: Look for the validation step that confirms secrets are configured

## 🚨 Troubleshooting

### Common Issues:

1. **"GOOGLE_CLOUD_PROJECT secret is not set"**
   - Make sure you added the `GOOGLE_CLOUD_PROJECT` secret
   - Check the secret name is exactly `GOOGLE_CLOUD_PROJECT`

2. **"Authentication failed"**
   - Verify the `GOOGLE_SERVICE_ACCOUNT_KEY` is valid JSON
   - Check the service account has the required permissions
   - Ensure the project ID matches

3. **"Bucket not found"**
   - Create the bucket: `gsutil mb gs://mlops-project-storage`
   - Check the bucket name matches the workflow configuration

4. **"Permission denied"**
   - Verify service account roles are correctly assigned
   - Check the service account is active

## 📞 Support

If you encounter issues:
1. Check the GitHub Actions logs for detailed error messages
2. Verify all secrets are correctly set
3. Ensure Google Cloud project and APIs are properly configured
4. Check the service account permissions

The workflow will now validate the configuration before proceeding with the build and deployment steps.