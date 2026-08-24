"""
utils.py
Shared utilities for the AI Vehicle Safety Classifier
Author: Corey Leath (CoreyLeath-code)
L5/L6 Production-Ready Version
"""

import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import yaml
import logging


# -------------------------------------------------------------
# Load Dataset
# -------------------------------------------------------------
def load_dataset(cfg):
    """
    Loads dataset from config path.
    Expected:
        data/
          images/
          labels.csv

    Returns:
        X: np.ndarray (images)
        y: np.ndarray (labels)
        class_names: list[str]
    """

    data_dir = cfg["data"]["path"]
    labels_file = cfg["data"]["labels"]

    labels_path = os.path.join(data_dir, labels_file)
    if not os.path.exists(labels_path):
        raise FileNotFoundError(f"Labels file not found: {labels_path}")

    import pandas as pd
    df = pd.read_csv(labels_path)

    img_paths, labels = df["image_path"].values, df["label"].values
    class_names = sorted(df["label"].unique())

    X = []
    for img_file in img_paths:
        img_path = os.path.join(data_dir, "images", img_file)
        image = cv2.imread(img_path)

        if image is None:
            logging.warning("Skipping corrupted or missing image: %s", img_path)
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, tuple(cfg["model"]["input_shape"][:2]))
        X.append(image)

    X = np.array(X)
    y = labels[: len(X)]

    logging.info("Loaded dataset:")
    logging.info("  Total images: %d", len(X))
    logging.info("  Classes: %s", class_names)

    return X, y, class_names


# -------------------------------------------------------------
# Preprocessing
# -------------------------------------------------------------
def preprocess_batch(batch):
    """Normalize images and scale to [0,1]."""
    batch = batch.astype("float32") / 255.0
    return batch


def preprocess_image(image, target_size=(224, 224)):
    """Preprocess a single image for inference."""
    if image is None:
        raise ValueError("Invalid image for preprocessing")

    resized = cv2.resize(image, target_size)
    normalized = resized.astype("float32") / 255.0
    return normalized


# -------------------------------------------------------------
# Build CNN Model
# -------------------------------------------------------------
def build_cnn_model(input_shape, num_classes, dropout_rate=0.3):
    """
    Builds a simple but powerful CNN for production-level classification.
    """

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),

        tf.keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Flatten(),

        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(dropout_rate),

        tf.keras.layers.Dense(num_classes, activation="softmax")
    ])

    logging.info("Model built with input shape %s and %d classes.", input_shape, num_classes)
    model.summary(print_fn=logging.info)

    return model


# -------------------------------------------------------------
# Model Versioning
# -------------------------------------------------------------
def save_model_with_versioning(model, cfg):
    """
    Saves the trained model in:
        models/v1/model_YYYY_MM_DD_HHMM.h5
    """
    version_dir = cfg["paths"]["model_dir"]
    os.makedirs(version_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M")
    model_name = f"vehicle_safety_model_{timestamp}.h5"
    model_path = os.path.join(version_dir, model_name)

    model.save(model_path)
    return model_path


def load_model(path):
    """Loads a saved TensorFlow model."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")

    return tf.keras.models.load_model(path)


# -------------------------------------------------------------
# Visualization Utilities
# -------------------------------------------------------------
def plot_training_metrics(history, output_dir):
    """Plots accuracy and loss curves."""
    os.makedirs(output_dir, exist_ok=True)

    # Accuracy
    plt.figure(figsize=(8, 5))
    plt.plot(history.history["accuracy"], label="Train Accuracy")
    plt.plot(history.history["val_accuracy"], label="Val Accuracy")
    plt.title("Training Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.savefig(os.path.join(output_dir, "accuracy_curve.png"))
    plt.close()

    # Loss
    plt.figure(figsize=(8, 5))
    plt.plot(history.history["loss"], label="Train Loss")
    plt.plot(history.history["val_loss"], label="Val Loss")
    plt.title("Training Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.savefig(os.path.join(output_dir, "loss_curve.png"))
    plt.close()


def plot_confusion_matrix(cm, class_names, output_dir):
    """Saves confusion matrix visualization."""
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=class_names,
                yticklabels=class_names)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.savefig(os.path.join(output_dir, "confusion_matrix.png"))
    plt.close()
