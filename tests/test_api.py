"""
Tests for the FastAPI model serving service
"""
import pytest
import numpy as np
from fastapi.testclient import TestClient
from src.serve import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code in [200, 503]  # 503 if model not loaded

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "MLOps Model Service" in response.json()["message"]

def test_predict_endpoint():
    """Test prediction endpoint with sample data"""
    # Create sample image data (32x32 grayscale)
    sample_image = np.random.rand(32, 32, 1).flatten().tolist()
    
    response = client.post(
        "/predict",
        json={
            "image_data": sample_image,
            "image_shape": [32, 32, 1]
        }
    )
    
    # Should return 200 or 503 (if model not loaded)
    assert response.status_code in [200, 503]
    
    if response.status_code == 200:
        data = response.json()
        assert "prediction" in data
        assert "confidence" in data
        assert "class_name" in data
        assert len(data["prediction"]) == 10  # CIFAR-10 has 10 classes
        assert 0 <= data["confidence"] <= 1

def test_predict_invalid_data():
    """Test prediction with invalid data"""
    response = client.post(
        "/predict",
        json={
            "image_data": "invalid",
            "image_shape": [32, 32, 1]
        }
    )
    assert response.status_code == 400

if __name__ == "__main__":
    pytest.main([__file__])