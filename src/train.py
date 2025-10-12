import os
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from src.utils.seed import set_seed
import mlflow
import mlflow.tensorflow


def load_data(data_dir):
    """Load prepared data."""
    x_train = np.load(os.path.join(data_dir, 'x_train.npy'))
    x_val = np.load(os.path.join(data_dir, 'x_val.npy'))
    y_train = np.load(os.path.join(data_dir, 'y_train.npy'))
    y_val = np.load(os.path.join(data_dir, 'y_val.npy'))
    
    return x_train, x_val, y_train, y_val


def create_model(params, input_shape, num_classes):
    """Create the CNN model."""
    model = Sequential([
        Conv2D(params['conv_size'], (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D(2, 2),
        Conv2D(params['conv_size'] * 2, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(params['conv_size'] * 4, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(params['dense_size'], activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    return model


def train_model(model, x_train, y_train, x_val, y_val, params):
    """Train the model with MLflow tracking."""
    # Setup MLflow tracking - use local storage
    try:
        mlflow.set_tracking_uri('file:./mlruns')
        mlflow.set_experiment('mlops-experiment')
        
        with mlflow.start_run():
            # Log parameters
            mlflow.log_params(params)
            
            # Compile model
            model.compile(
                optimizer=Adam(learning_rate=params['lr']),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )
            
            # Callbacks
            callbacks = [
                EarlyStopping(patience=3, restore_best_weights=True),
                ReduceLROnPlateau(factor=0.5, patience=2)
            ]
            
            # Train model
            history = model.fit(
                x_train, y_train,
                validation_data=(x_val, y_val),
                epochs=params['epochs'],
                batch_size=32,
                callbacks=callbacks,
                verbose=1
            )
            
            # Log metrics
            mlflow.log_metric("final_train_loss", history.history['loss'][-1])
            mlflow.log_metric("final_train_accuracy", history.history['accuracy'][-1])
            mlflow.log_metric("final_val_loss", history.history['val_loss'][-1])
            mlflow.log_metric("final_val_accuracy", history.history['val_accuracy'][-1])
            
            # Log model
            mlflow.tensorflow.log_model(
                model,
                "model",
                registered_model_name="cifar10-cnn"
            )
            
            return history
    except Exception as e:
        print(f"MLflow error: {e}")
        print("Continuing without MLflow tracking...")
        
        # Fallback: train without MLflow
        model.compile(
            optimizer=Adam(learning_rate=params['lr']),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        callbacks = [
            EarlyStopping(patience=3, restore_best_weights=True),
            ReduceLROnPlateau(factor=0.5, patience=2)
        ]
        
        history = model.fit(
            x_train, y_train,
            validation_data=(x_val, y_val),
            epochs=params['epochs'],
            batch_size=32,
            callbacks=callbacks,
            verbose=1
        )
        
        return history


def save_model(model, history, output_dir):
    """Save the trained model and training history."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    model.save(os.path.join(output_dir, 'model.h5'))
    
    # Save training history
    history_dict = {
        'loss': history.history['loss'],
        'accuracy': history.history['accuracy'],
        'val_loss': history.history['val_loss'],
        'val_accuracy': history.history['val_accuracy']
    }
    
    import json
    with open(os.path.join(output_dir, 'history.json'), 'w') as f:
        json.dump(history_dict, f)
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'training_history.png'))
    plt.close()


def main():
    if len(sys.argv) != 3:
        print("Usage: python train.py <data_dir> <model_dir>")
        sys.exit(1)
    
    data_dir = sys.argv[1]
    model_dir = sys.argv[2]
    
    # Load parameters
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
    
    # Set seed for reproducibility
    set_seed(params['train']['seed'])
    
    print("Loading data...")
    x_train, x_val, y_train, y_val = load_data(data_dir)
    
    print("Creating model...")
    input_shape = x_train.shape[1:]
    num_classes = params['train']['output_classes']
    model = create_model(params['train'], input_shape, num_classes)
    
    print("Training model...")
    history = train_model(model, x_train, y_train, x_val, y_val, params['train'])
    
    print("Saving model...")
    save_model(model, history, model_dir)
    
    print("Training complete!")


if __name__ == "__main__":
    main()