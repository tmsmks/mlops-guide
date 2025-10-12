"""
MLflow configuration for cloud deployment
"""
import os
import mlflow
import mlflow.tensorflow
from google.cloud import storage
from google.cloud import aiplatform

def setup_mlflow_tracking():
    """Setup MLflow tracking with Google Cloud Storage backend"""
    # Set MLflow tracking URI to use Google Cloud Storage
    tracking_uri = os.getenv('MLFLOW_TRACKING_URI', 'gs://mlops-project-storage/mlflow')
    mlflow.set_tracking_uri(tracking_uri)
    
    # Set experiment name
    experiment_name = os.getenv('MLFLOW_EXPERIMENT_NAME', 'mlops-experiment')
    mlflow.set_experiment(experiment_name)
    
    return mlflow

def setup_mlflow_model_registry():
    """Setup MLflow model registry"""
    registry_uri = os.getenv('MLFLOW_REGISTRY_URI', 'gs://mlops-project-storage/mlflow-registry')
    mlflow.set_registry_uri(registry_uri)
    
    return mlflow

def log_model_to_registry(model, model_name, model_version="1.0.0"):
    """Log model to MLflow model registry"""
    with mlflow.start_run():
        # Log model
        mlflow.tensorflow.log_model(
            model,
            "model",
            registered_model_name=model_name
        )
        
        # Log model version
        client = mlflow.tracking.MlflowClient()
        client.create_model_version(
            name=model_name,
            source=f"gs://mlops-project-storage/mlflow/{mlflow.active_run().info.run_id}/artifacts/model",
            run_id=mlflow.active_run().info.run_id
        )
        
        return model_name, model_version