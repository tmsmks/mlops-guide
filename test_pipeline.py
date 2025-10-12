#!/usr/bin/env python3
"""
End-to-end pipeline test script
"""
import os
import sys
import subprocess
import time
import requests
import json
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Command failed: {cmd}")
            print(f"Error: {result.stderr}")
            return False
        print(f"✅ Command succeeded: {cmd}")
        return True
    except Exception as e:
        print(f"❌ Command error: {cmd} - {e}")
        return False

def test_data_preparation():
    """Test data preparation pipeline"""
    print("\n🔍 Testing data preparation...")
    
    # Check if data directory exists
    if not os.path.exists("data/prepared"):
        print("❌ Prepared data directory not found")
        return False
    
    # Check if required files exist
    required_files = ["x_train.npy", "x_val.npy", "y_train.npy", "y_val.npy", "label_encoder.pkl", "labels.json"]
    for file in required_files:
        if not os.path.exists(f"data/prepared/{file}"):
            print(f"❌ Required file not found: {file}")
            return False
    
    print("✅ Data preparation files found")
    return True

def test_model_training():
    """Test model training"""
    print("\n🔍 Testing model training...")
    
    # Check if model directory exists
    if not os.path.exists("model"):
        print("❌ Model directory not found")
        return False
    
    # Check if model file exists
    if not os.path.exists("model/model.h5"):
        print("❌ Model file not found")
        return False
    
    print("✅ Model training completed")
    return True

def test_model_evaluation():
    """Test model evaluation"""
    print("\n🔍 Testing model evaluation...")
    
    # Check if evaluation directory exists
    if not os.path.exists("evaluation"):
        print("❌ Evaluation directory not found")
        return False
    
    # Check if metrics file exists
    if not os.path.exists("evaluation/metrics.json"):
        print("❌ Metrics file not found")
        return False
    
    # Check if plots exist
    plots_dir = "evaluation/plots"
    if not os.path.exists(plots_dir):
        print("❌ Plots directory not found")
        return False
    
    required_plots = ["confusion_matrix.png", "pred_preview.png", "training_history.png"]
    for plot in required_plots:
        if not os.path.exists(f"{plots_dir}/{plot}"):
            print(f"❌ Required plot not found: {plot}")
            return False
    
    print("✅ Model evaluation completed")
    return True

def test_api_service():
    """Test API service"""
    print("\n🔍 Testing API service...")
    
    # Start the service in background
    print("Starting API service...")
    process = subprocess.Popen([sys.executable, "src/serve.py"], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
    
    # Wait for service to start
    time.sleep(10)
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code in [200, 503]:  # 503 if model not loaded
            print("✅ API service is running")
        else:
            print(f"❌ API service health check failed: {response.status_code}")
            return False
        
        # Test root endpoint
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ API root endpoint working")
        else:
            print(f"❌ API root endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API service test failed: {e}")
        return False
    finally:
        # Stop the service
        process.terminate()
        process.wait()

def test_dvc_configuration():
    """Test DVC configuration"""
    print("\n🔍 Testing DVC configuration...")
    
    # Check DVC remote configuration
    result = subprocess.run(["python", "-m", "dvc", "remote", "list"], 
                          capture_output=True, text=True)
    
    if "storage" in result.stdout:
        print("✅ DVC remote configured")
        return True
    else:
        print("❌ DVC remote not configured")
        return False

def test_mlflow_configuration():
    """Test MLflow configuration"""
    print("\n🔍 Testing MLflow configuration...")
    
    # Check if mlflow_config.py exists
    if not os.path.exists("mlflow_config.py"):
        print("❌ MLflow configuration file not found")
        return False
    
    print("✅ MLflow configuration found")
    return True

def main():
    """Run all tests"""
    print("🚀 Starting MLOps Pipeline Tests")
    print("=" * 50)
    
    tests = [
        ("DVC Configuration", test_dvc_configuration),
        ("MLflow Configuration", test_mlflow_configuration),
        ("Data Preparation", test_data_preparation),
        ("Model Training", test_model_training),
        ("Model Evaluation", test_model_evaluation),
        ("API Service", test_api_service),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Pipeline is ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())