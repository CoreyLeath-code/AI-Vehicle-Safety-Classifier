"""
AI Vehicle Safety Classifier — Training Pipeline
Author: Corey Leath (CoreyLeath-code)
L5/L6 Production-Ready Architecture

Handles:
✔ Model creation (custom CNN or transfer learning)
✔ Data loading via ImageDataGenerators
✔ Early stopping + checkpointing
✔ Training history saving
✔ Evaluation + metrics export
"""

import os
import yaml
import pickle
import tensorflow as tf

from model import create_model
from data import build_generators


# ---------------------------------------------------------------------
# Load config
# ---------------------------------------------------------------------
def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------
# Train the model
# ---------------------------------------------------------------------
def train_model(config_path="config/config.yaml", use_transfer_learning=False):

    # Load configuration
    config = load_config(config_path)

    # Load data
    train_gen, val_gen, test_gen = build_generators(config_path)

    # Load/create model
    model = create_model(config_path=config_path,
                         use_transfer_learning=use_transfer_learning)

    # Create training dirs
    model_dir = config["paths"]["model_dir"]
    os.makedirs(model_dir, exist_ok=True)

    # -----------------------------------------------------------------
    # Callbacks — L6 professional pipeline
    # -----------------------------------------------------------------
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=config["training"]["early_stopping_patience"],
        restore_best_weights=True
    )

    checkpoint_path = os.path.join(model_dir, "best_model.keras")
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        save_best_only=True,
        save_weights_only=False,
        monitor="val_loss",
        mode="min"
    )

    # -----------------------------------------------------------------
    # Train model
    # -----------------------------------------------------------------
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=config["training"]["epochs"],
        callbacks=[early_stop, checkpoint],
        verbose=1
    )

    # -----------------------------------------------------------------
    # Save training history for plotting later
    # -----------------------------------------------------------------
    history_path = os.path.join(model_dir, "training_history.pkl")
    with open(history_path, "wb") as f:
        pickle.dump(history.history, f)

    # -----------------------------------------------------------------
    # Evaluate on test set
    # -----------------------------------------------------------------
    test_loss, test_acc = model.evaluate(test_gen, verbose=1)

    # -----------------------------------------------------------------
    # Save evaluation metrics
    # -----------------------------------------------------------------
    metrics_path = os.path.join(model_dir, "metrics.txt")
    with open(metrics_path, "w") as f:
        f.write(f"Test Accuracy: {test_acc:.4f}\n")
        f.write(f"Test Loss: {test_loss:.4f}\n")

    print("\nTraining complete!")
    print(f"Best model saved to: {checkpoint_path}")
    print(f"Metrics saved to:   {metrics_path}")
    print(f"History saved to:   {history_path}")

    return model
