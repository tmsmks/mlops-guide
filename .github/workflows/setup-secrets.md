# GitHub Secrets Setup for machledata-474307

## 🔐 Required Secrets

Add these secrets to your GitHub repository:

### 1. GOOGLE_SERVICE_ACCOUNT_KEY
- **Name**: `GOOGLE_SERVICE_ACCOUNT_KEY`
- **Value**: Run `./setup_gcp.sh` to generate the credentials.json file, then copy its content

### 2. GOOGLE_CLOUD_PROJECT
- **Name**: `GOOGLE_CLOUD_PROJECT`
- **Value**: `machledata-474307`

## 🚀 Quick Setup

1. **Run the setup script:**
   ```bash
   ./setup_gcp.sh
   ```

2. **Add secrets to GitHub:**
   - Go to: https://github.com/tmsmks/mlops-guide/settings/secrets/actions
   - Add the two secrets above

3. **Test the workflow:**
   - Push a commit or manually trigger the workflow
   - Check the Actions tab for results

## 📋 What the setup script does:

- ✅ Sets project to `machledata-474307`
- ✅ Enables required Google Cloud APIs
- ✅ Creates service account `mlops-service-account`
- ✅ Grants necessary permissions
- ✅ Creates storage bucket `gs://mlops-project-storage`
- ✅ Generates service account key file

## 🔧 Manual Setup (if needed)

If you prefer to set up manually:

```bash
# Set project
gcloud config set project machledata-474307

# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com storage.googleapis.com aiplatform.googleapis.com containerregistry.googleapis.com

# Create service account
gcloud iam service-accounts create mlops-service-account --display-name="MLOps Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding machledata-474307 --member="serviceAccount:mlops-service-account@machledata-474307.iam.gserviceaccount.com" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding machledata-474307 --member="serviceAccount:mlops-service-account@machledata-474307.iam.gserviceaccount.com" --role="roles/run.admin"
gcloud projects add-iam-policy-binding machledata-474307 --member="serviceAccount:mlops-service-account@machledata-474307.iam.gserviceaccount.com" --role="roles/aiplatform.user"
gcloud projects add-iam-policy-binding machledata-474307 --member="serviceAccount:mlops-service-account@machledata-474307.iam.gserviceaccount.com" --role="roles/cloudbuild.builds.builder"

# Create bucket
gsutil mb gs://mlops-project-storage

# Create key
gcloud iam service-accounts keys create credentials.json --iam-account=mlops-service-account@machledata-474307.iam.gserviceaccount.com
```

## ✅ Verification

After setup, the workflow should:
1. ✅ Validate secrets are configured
2. ✅ Build and test the application  
3. ✅ Deploy to Google Cloud Run
4. ✅ Generate monitoring reports