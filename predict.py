"""Deterministic vehicle-condition scoring and optional CNN image inference."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final

import yaml

_WEATHER_PENALTY: Final = {"clear": 0, "sunny": 0, "rain": 20, "snow": 25, "fog": 30}
_VISIBILITY_PENALTY: Final = {"high": 0, "medium": 15, "low": 30}
_TRAFFIC_PENALTY: Final = {"light": 0, "moderate": 10, "heavy": 20}
_DRIVER_PENALTY: Final = {"alert": 0, "distracted": 20, "drowsy": 30}


def load_config(config_path: str = "config/config.yaml") -> dict:
    """Load a non-empty YAML mapping."""
    with Path(config_path).open(encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
    if not isinstance(config, dict):
        raise ValueError("configuration must be a YAML mapping")
    return config


def load_best_model(config_path: str = "config/config.yaml"):
    """Load the trained TensorFlow artifact lazily."""
    import tensorflow as tf

    model_dir = load_config(config_path)["paths"]["model_dir"]
    model_path = Path(model_dir) / "best_model.keras"
    if not model_path.is_file():
        raise FileNotFoundError(f"model artifact not found: {model_path}")
    return tf.keras.models.load_model(model_path)


def preprocess_image(img_path: str, config_path: str = "config/config.yaml"):
    """Decode, normalize, and batch one image."""
    import numpy as np
    from tensorflow.keras.preprocessing import image

    target = tuple(load_config(config_path)["model"]["input_shape"][:2])
    source = Path(img_path)
    if not source.is_file():
        raise FileNotFoundError(f"input image not found: {source}")
    img = image.load_img(source, target_size=target)
    return np.expand_dims(image.img_to_array(img) / 255.0, axis=0)


def predict_image(img_path: str, config_path: str = "config/config.yaml") -> dict:
    """Return the class and confidence for an image."""
    import numpy as np

    model = load_best_model(config_path)
    config = load_config(config_path)
    predictions = model.predict(preprocess_image(img_path, config_path), verbose=0)
    index = int(np.argmax(predictions, axis=1)[0])
    confidence = float(predictions[0][index])

    mapping_path = Path(config["paths"]["model_dir"]) / "label_mapping.txt"
    labels = {}
    with mapping_path.open(encoding="utf-8") as stream:
        for line in stream:
            raw_index, label = line.strip().split(": ", maxsplit=1)
            labels[int(raw_index)] = label
    if index not in labels:
        raise ValueError(f"label mapping is missing class index {index}")
    return {"predicted_class": labels[index], "confidence": confidence}


def _validated(value: str, field: str, options: dict[str, int]) -> str:
    normalized = str(value).strip().lower()
    if normalized not in options:
        allowed = ", ".join(sorted(options))
        raise ValueError(f"{field} must be one of: {allowed}")
    return normalized


def classify_driving_conditions(
    weather: str,
    visibility: str,
    traffic: str,
    driver_state: str,
) -> tuple[int, str, str]:
    """Score a validated scenario on a deterministic 0–100 safety scale."""
    weather = _validated(weather, "weather", _WEATHER_PENALTY)
    visibility = _validated(visibility, "visibility", _VISIBILITY_PENALTY)
    traffic = _validated(traffic, "traffic", _TRAFFIC_PENALTY)
    driver_state = _validated(driver_state, "driver_state", _DRIVER_PENALTY)
    penalty = (
        _WEATHER_PENALTY[weather]
        + _VISIBILITY_PENALTY[visibility]
        + _TRAFFIC_PENALTY[traffic]
        + _DRIVER_PENALTY[driver_state]
    )
    score = max(0, 100 - penalty)
    if score >= 70:
        return score, "low", "Driving conditions are safe. No major risk factors detected."
    if score >= 40:
        return score, "medium", "Moderate risk detected. Exercise caution while driving."
    return score, "high", "High risk conditions detected. Driving is not recommended."


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Predict vehicle safety from an image")
    parser.add_argument("image_path")
    parser.add_argument("--config", default=os.getenv("CONFIG_PATH", "config/config.yaml"))
    args = parser.parse_args()
    print(predict_image(args.image_path, args.config))
