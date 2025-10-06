import os
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import load_model
import json


def load_data_and_model(data_dir, model_dir):
    """Load test data and trained model."""
    # Load data
    x_val = np.load(os.path.join(data_dir, 'x_val.npy'))
    y_val = np.load(os.path.join(data_dir, 'y_val.npy'))
    
    # Load label encoder
    import pickle
    with open(os.path.join(data_dir, 'label_encoder.pkl'), 'rb') as f:
        le = pickle.load(f)
    
    # Load model
    model = load_model(os.path.join(model_dir, 'model.h5'))
    
    return x_val, y_val, le, model


def evaluate_model(model, x_val, y_val, le):
    """Evaluate the model and return metrics."""
    # Make predictions
    y_pred_proba = model.predict(x_val)
    y_pred = np.argmax(y_pred_proba, axis=1)
    
    # Calculate metrics
    val_loss, val_accuracy = model.evaluate(x_val, y_val, verbose=0)
    
    # Classification report
    class_names = le.classes_
    report = classification_report(y_val, y_pred, target_names=class_names, output_dict=True)
    
    return {
        'val_loss': float(val_loss),
        'val_acc': float(val_accuracy),
        'classification_report': report
    }, y_pred, y_pred_proba


def plot_confusion_matrix(y_true, y_pred, class_names, output_path):
    """Plot and save confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_prediction_samples(x_val, y_val, y_pred, y_pred_proba, le, output_path, num_samples=8):
    """Plot sample predictions."""
    class_names = le.classes_
    
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    axes = axes.ravel()
    
    for i in range(min(num_samples, len(x_val))):
        axes[i].imshow(x_val[i].squeeze(), cmap='gray' if x_val[i].shape[-1] == 1 else None)
        axes[i].set_title(f'True: {class_names[y_val[i]]}\nPred: {class_names[y_pred[i]]} ({y_pred_proba[i][y_pred[i]]:.2f})')
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_training_history(model_dir, output_path):
    """Plot training history."""
    # Load training history
    with open(os.path.join(model_dir, 'history.json'), 'r') as f:
        history = json.load(f)
    
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history['loss'], label='Training Loss')
    plt.plot(history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history['accuracy'], label='Training Accuracy')
    plt.plot(history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def save_metrics(metrics, output_path):
    """Save evaluation metrics."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save only the main metrics (not the full classification report)
    main_metrics = {
        'val_loss': metrics['val_loss'],
        'val_acc': metrics['val_acc']
    }
    
    with open(output_path, 'w') as f:
        json.dump(main_metrics, f, indent=2)


def main():
    if len(sys.argv) != 3:
        print("Usage: python evaluate.py <model_dir> <data_dir>")
        sys.exit(1)
    
    model_dir = sys.argv[1]
    data_dir = sys.argv[2]
    
    print("Loading data and model...")
    x_val, y_val, le, model = load_data_and_model(data_dir, model_dir)
    
    print("Evaluating model...")
    metrics, y_pred, y_pred_proba = evaluate_model(model, x_val, y_val, le)
    
    print("Creating plots...")
    os.makedirs('evaluation/plots', exist_ok=True)
    
    # Plot confusion matrix
    plot_confusion_matrix(y_val, y_pred, le.classes_, 'evaluation/plots/confusion_matrix.png')
    
    # Plot prediction samples
    plot_prediction_samples(x_val, y_val, y_pred, y_pred_proba, le, 'evaluation/plots/pred_preview.png')
    
    # Plot training history
    plot_training_history(model_dir, 'evaluation/plots/training_history.png')
    
    # Save metrics
    save_metrics(metrics, 'evaluation/metrics.json')
    
    print(f"Evaluation complete! Validation accuracy: {metrics['val_acc']:.4f}")


if __name__ == "__main__":
    main()