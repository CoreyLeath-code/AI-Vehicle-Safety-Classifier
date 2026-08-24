"""
AI Vehicle Safety Classifier — Evaluation Module
Author: Corey Leath (CoreyLeath-code)
L5/L6 Production-Ready Architecture

Handles:
✔ Model loading
✔ Test set predictions
✔ Confusion matrix (PNG)
✔ Classification report (TXT)
✔ ROC-AUC (multi-class compatible)
✔ Saves all evaluation outputs for README badges
"""

import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    roc_auc_score
)


# ---------------------------------------------------------------------
# Load config
# ---------------------------------------------------------------------
def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------
# Load model
# ---------------------------------------------------------------------
def load_best_model(model_path):
    return tf.keras.models.load_model(model_path)


# ---------------------------------------------------------------------
# Evaluate model
# ---------------------------------------------------------------------
def evaluate_model(config_path="config/config.yaml"):

    config = load_config(config_path)

    # Load paths
    model_dir = config["paths"]["model_dir"]
    best_model_path = os.path.join(model_dir, "best_model.keras")

    # Load saved model
    model = load_best_model(best_model_path)

    # Load data generators
    from data import build_generators
    _, _, test_gen = build_generators(config_path)

    # Predict
    predictions = model.predict(test_gen, verbose=1)
    y_pred = np.argmax(predictions, axis=1)
    y_true = test_gen.classes
    labels = list(test_gen.class_indices.keys())

    # ---------------------------------------------------------------
    # Classification report
    # ---------------------------------------------------------------
    report = classification_report(
        y_true, y_pred, target_names=labels, output_dict=False
    )

    report_path = os.path.join(model_dir, "classification_report.txt")
    with open(report_path, "w") as f:
        f.write(report)

    print("\nClassification Report:")
    print(report)

    # ---------------------------------------------------------------
    # Confusion matrix
    # ---------------------------------------------------------------
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

    plt.figure(figsize=(8, 6))
    disp.plot(cmap="Blues", values_format="d")
    plt.title("Confusion Matrix — AI Vehicle Safety Classifier")
    plt.tight_layout()

    cm_path = os.path.join(model_dir, "confusion_matrix.png")
    plt.savefig(cm_path)
    plt.close()

    # ---------------------------------------------------------------
    # Multi-class ROC AUC
    # ---------------------------------------------------------------
    try:
        auc = roc_auc_score(
            y_true,
            predictions,
            multi_class="ovr"
        )
    except:
        auc = None

    auc_path = os.path.join(model_dir, "auc_score.txt")
    with open(auc_path, "w") as f:
        if auc:
            f.write(f"ROC-AUC Score: {auc:.4f}")
        else:
            f.write("ROC-AUC Score: Not applicable (requires >2 classes)")

    # ---------------------------------------------------------------
    # Label map export (for inference)
    # ---------------------------------------------------------------
    label_map_path = os.path.join(model_dir, "label_mapping.txt")
    with open(label_map_path, "w") as f:
        for label, idx in test_gen.class_indices.items():
            f.write(f"{idx}: {label}\n")

    # ---------------------------------------------------------------
    # Summary print
    # ---------------------------------------------------------------
    print("\nEvaluation complete!")
    print(f"- Classification report saved to: {report_path}")
    print(f"- Confusion matrix saved to:     {cm_path}")
    print(f"- AUC score saved to:            {auc_path}")
    print(f"- Label mapping saved to:        {label_map_path}")

    return {
        "y_true": y_true,
        "y_pred": y_pred,
        "labels": labels
    }
