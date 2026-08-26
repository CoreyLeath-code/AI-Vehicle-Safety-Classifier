"""
AI Vehicle Safety Classifier — Model Builder
Author: Corey Leath (CoreyLeath-code)
L5/L6 Production-Ready Architecture

This file creates and compiles the CNN model using configuration
settings from config.yaml. Supports both custom CNN and transfer
learning (MobileNetV2) for higher accuracy.
"""

import yaml
import os
import tensorflow as tf
from tensorflow.keras import layers, models


# ---------------------------------------------------------------------
# Load Configuration
# ---------------------------------------------------------------------
def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------
# Build a Custom CNN Model
# ---------------------------------------------------------------------
def build_custom_cnn(config):
    input_shape = tuple(config["model"]["input_shape"])
    num_classes = config["model"]["num_classes"]
    dropout_rate = config["model"]["dropout_rate"]
    learning_rate = config["model"]["learning_rate"]

    model = models.Sequential([
        layers.Input(shape=input_shape),

        layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(dropout_rate),

        layers.Dense(num_classes, activation="softmax")
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# ---------------------------------------------------------------------
# Build a Transfer Learning Model (MobileNetV2)
# ---------------------------------------------------------------------
def build_transfer_learning_model(config):
    input_shape = tuple(config["model"]["input_shape"])
    num_classes = config["model"]["num_classes"]
    learning_rate = config["model"]["learning_rate"]

    base = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet"
    )
    base.trainable = False  # Freeze base for fast training

    model = models.Sequential([
        base,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="softmax")
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# ---------------------------------------------------------------------
# Model Builder Router
# ---------------------------------------------------------------------
def create_model(config_path="config/config.yaml", use_transfer_learning=False):

    config = load_config(config_path)

    if use_transfer_learning:
        model = build_transfer_learning_model(config)
    else:
        model = build_custom_cnn(config)

    # Save model summary to file
    model_dir = config["paths"]["model_dir"]
    os.makedirs(model_dir, exist_ok=True)

    summary_path = os.path.join(model_dir, "model_summary.txt")
    with open(summary_path, "w") as f:
        model.summary(print_fn=lambda x: f.write(x + "\n"))

    return model
