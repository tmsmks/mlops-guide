#!/usr/bin/env python3
"""
Validation script for MLOps cloud setup
"""
import os
import sys
import subprocess
import yaml
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NOT FOUND")
        return False

def check_dvc_config():
    """Check DVC configuration"""
    print("\n🔍 Checking DVC configuration...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "dvc", "config", "--list"], 
                              capture_output=True, text=True)
        
        if "remote.storage.url" in result.stdout:
            print("✅ DVC remote storage configured")
            return True
        else:
            print("❌ DVC remote storage not configured")
            return False
    except Exception as e:
        print(f"❌ DVC configuration check failed: {e}")
        return False

def check_requirements():
    """Check if all required packages are installed"""
    print("\n🔍 Checking Python requirements...")
    
    required_packages = [
        "tensorflow", "mlflow", "fastapi", "dvc", 
        "google-cloud-storage", "google-cloud-aiplatform"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def check_project_structure():
    """Check if all required files and directories exist"""
    print("\n🔍 Checking project structure...")
    
    required_files = [
        "src/prepare.py",
        "src/train.py", 
        "src/evaluate.py",
        "src/serve.py",
        "src/monitor.py",
        "mlflow_config.py",
        "Dockerfile",
        "docker-compose.yml",
        "deploy.sh",
        "params.yaml",
        "dvc.yaml",
        "requirements.txt"
    ]
    
    required_dirs = [
        "src",
        "src/utils",
        "data",
        "evaluation",
        "tests",
        ".github/workflows"
    ]
    
    all_good = True
    
    for filepath in required_files:
        if not check_file_exists(filepath, "File"):
            all_good = False
    
    for dirpath in required_dirs:
        if not check_file_exists(dirpath, "Directory"):
            all_good = False
    
    return all_good

def check_github_workflow():
    """Check GitHub Actions workflow configuration"""
    print("\n🔍 Checking GitHub Actions workflow...")
    
    workflow_file = ".github/workflows/mlops.yaml"
    if not os.path.exists(workflow_file):
        print(f"❌ GitHub workflow not found: {workflow_file}")
        return False
    
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    required_elements = [
        "google-github-actions/auth",
        "mlflow",
        "docker build",
        "gcloud run deploy",
        "Cloud Run"
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing workflow elements: {', '.join(missing_elements)}")
        return False
    
    print("✅ GitHub Actions workflow properly configured")
    return True

def check_docker_configuration():
    """Check Docker configuration"""
    print("\n🔍 Checking Docker configuration...")
    
    if not check_file_exists("Dockerfile", "Dockerfile"):
        return False
    
    if not check_file_exists("docker-compose.yml", "Docker Compose file"):
        return False
    
    # Check if Dockerfile has required elements
    with open("Dockerfile", 'r') as f:
        dockerfile_content = f.read()
    
    required_docker_elements = [
        "FROM python:3.12-slim",
        "COPY requirements.txt",
        "EXPOSE 8000",
        "CMD"
    ]
    
    missing_elements = []
    for element in required_docker_elements:
        if element not in dockerfile_content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing Dockerfile elements: {', '.join(missing_elements)}")
        return False
    
    print("✅ Docker configuration complete")
    return True

def main():
    """Run all validation checks"""
    print("🚀 MLOps Cloud Setup Validation")
    print("=" * 50)
    
    checks = [
        ("Project Structure", check_project_structure),
        ("Python Requirements", check_requirements),
        ("DVC Configuration", check_dvc_config),
        ("Docker Configuration", check_docker_configuration),
        ("GitHub Workflow", check_github_workflow),
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n📋 Running: {check_name}")
        if check_func():
            passed += 1
        else:
            print(f"❌ {check_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Validation Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All validations passed! Your MLOps cloud setup is ready.")
        print("\n📋 Next steps:")
        print("1. Configure GitHub secrets (see .github/SECRETS.md)")
        print("2. Set up Google Cloud project and bucket")
        print("3. Run: dvc repro")
        print("4. Test locally: docker-compose up")
        print("5. Deploy: ./deploy.sh")
        return 0
    else:
        print("⚠️  Some validations failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())