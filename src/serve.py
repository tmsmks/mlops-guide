"""
FastAPI service for model serving
"""
import os
import sys
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import mlflow.tensorflow
from mlflow_config import setup_mlflow_tracking

app = FastAPI(title="MLOps Model Service", version="1.0.0")

# Global model variable
model = None

class PredictionRequest(BaseModel):
    image_data: list
    image_shape: list

class PredictionResponse(BaseModel):
    prediction: list
    confidence: float
    class_name: str

def load_model_from_registry():
    """Load the latest model from MLflow registry"""
    setup_mlflow_tracking()
    
    client = mlflow.tracking.MlflowClient()
    
    # Get the latest version of the model
    latest_version = client.get_latest_versions("cifar10-cnn", stages=["None"])[0]
    
    # Load model
    model_uri = f"models:/cifar10-cnn/{latest_version.version}"
    model = mlflow.tensorflow.load_model(model_uri)
    
    return model

@app.on_event("startup")
async def load_model():
    """Load model on startup"""
    global model
    try:
        model = load_model_from_registry()
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        # Fallback to local model if registry fails
        model_path = "model/model.h5"
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            print("Loaded local model as fallback")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "MLOps Model Service is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make prediction on image data"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert list to numpy array and reshape
        image_array = np.array(request.image_data).reshape(request.image_shape)
        
        # Add batch dimension
        image_batch = np.expand_dims(image_array, axis=0)
        
        # Make prediction
        prediction = model.predict(image_batch)
        
        # Get class with highest probability
        predicted_class = np.argmax(prediction[0])
        confidence = float(np.max(prediction[0]))
        
        # Map class index to class name (CIFAR-10 classes)
        class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
                      'dog', 'frog', 'horse', 'ship', 'truck']
        
        class_name = class_names[predicted_class] if predicted_class < len(class_names) else f"class_{predicted_class}"
        
        return PredictionResponse(
            prediction=prediction[0].tolist(),
            confidence=confidence,
            class_name=class_name
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)