"""
AI Vehicle Safety Classifier — Data Loader & Preprocessing
Author: Corey Leath (CoreyLeath-code)
L5/L6 Production-Ready Architecture

Handles:
✔ Loading dataset from directory
✔ Train/val/test preprocessing
✔ Image augmentation
✔ Config-driven pipeline
"""

import os
import yaml
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator


# ------------------------------------------------------------
# Load configuration
# ------------------------------------------------------------
def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------
# Build image generators
# ------------------------------------------------------------
def build_generators(config_path="config/config.yaml"):

    config = load_config(config_path)

    train_dir = config["paths"]["train_dir"]
    val_dir = config["paths"]["val_dir"]
    test_dir = config["paths"]["test_dir"]

    img_size = tuple(config["model"]["input_shape"][:2])
    batch_size = config["training"]["batch_size"]

    # --------------------------------------------------------
    # Augmentation for training
    # --------------------------------------------------------
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode="nearest"
    )

    # No augmentation for validation/test
    test_datagen = ImageDataGenerator(rescale=1.0 / 255)

    # --------------------------------------------------------
    # Train generator
    # --------------------------------------------------------
    train_gen = train_datagen.flow_from_directory(
        train_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode="sparse",
        shuffle=True
    )

    # --------------------------------------------------------
    # Validation generator
    # --------------------------------------------------------
    val_gen = test_datagen.flow_from_directory(
        val_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode="sparse",
        shuffle=False
    )

    # --------------------------------------------------------
    # Test generator
    # --------------------------------------------------------
    test_gen = test_datagen.flow_from_directory(
        test_dir,
        target_size=img_size,
        batch_size=1,
        class_mode="sparse",
        shuffle=False
    )

    return train_gen, val_gen, test_gen
