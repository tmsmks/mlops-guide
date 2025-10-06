import os
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from src.utils.seed import set_seed


def load_data():
    """Load CIFAR-10 dataset."""
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    
    # Combine train and test data
    x = np.concatenate([x_train, x_test])
    y = np.concatenate([y_train, y_test])
    
    return x, y


def preprocess_data(x, y, params):
    """Preprocess the data according to parameters."""
    # Set seed for reproducibility
    set_seed(params['seed'])
    
    # Convert to grayscale if specified
    if params['grayscale']:
        x = np.mean(x, axis=3, keepdims=True)
    
    # Resize images
    target_size = tuple(params['image_size'])
    x_resized = []
    for img in x:
        img_resized = tf.image.resize(img, target_size).numpy()
        x_resized.append(img_resized)
    x = np.array(x_resized)
    
    # Normalize pixel values
    x = x.astype('float32') / 255.0
    
    # Encode labels
    le = LabelEncoder()
    y = le.fit_transform(y.flatten())
    
    return x, y, le


def split_data(x, y, params):
    """Split data into train and validation sets."""
    x_train, x_val, y_train, y_val = train_test_split(
        x, y, 
        test_size=params['split'], 
        random_state=params['seed'],
        stratify=y
    )
    
    return x_train, x_val, y_train, y_val


def save_data(x_train, x_val, y_train, y_val, le, output_dir):
    """Save processed data."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save data arrays
    np.save(os.path.join(output_dir, 'x_train.npy'), x_train)
    np.save(os.path.join(output_dir, 'x_val.npy'), x_val)
    np.save(os.path.join(output_dir, 'y_train.npy'), y_train)
    np.save(os.path.join(output_dir, 'y_val.npy'), y_val)
    
    # Save label encoder
    import pickle
    with open(os.path.join(output_dir, 'label_encoder.pkl'), 'wb') as f:
        pickle.dump(le, f)
    
    # Save labels info
    labels_info = {
        'class_names': le.classes_.tolist(),
        'num_classes': len(le.classes_)
    }
    with open(os.path.join(output_dir, 'labels.json'), 'w') as f:
        yaml.dump(labels_info, f, default_flow_style=False)


def main():
    if len(sys.argv) != 3:
        print("Usage: python prepare.py <input_dir> <output_dir>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Load parameters
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
    
    print("Loading data...")
    x, y = load_data()
    
    print("Preprocessing data...")
    x, y, le = preprocess_data(x, y, params['prepare'])
    
    print("Splitting data...")
    x_train, x_val, y_train, y_val = split_data(x, y, params['prepare'])
    
    print("Saving data...")
    save_data(x_train, x_val, y_train, y_val, le, output_dir)
    
    print(f"Data preparation complete. Train samples: {len(x_train)}, Validation samples: {len(x_val)}")


if __name__ == "__main__":
    main()