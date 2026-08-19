"""Shared configuration, logging, and filesystem helpers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path = "config/config.yaml") -> dict[str, Any]:
    """Load YAML configuration from *path*."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def ensure_directories(config: dict[str, Any]) -> None:
    """Create configured output directories when they do not exist."""
    paths = [
        config["data"]["processed_path"],
        config["paths"]["models_dir"],
        config["paths"]["figures_dir"],
        config["paths"]["tables_dir"],
        config["paths"]["predictions_dir"],
    ]
    for path in paths:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        if Path(path).suffix == "":
            Path(path).mkdir(parents=True, exist_ok=True)


def get_logger(name: str = "aquaponic") -> logging.Logger:
    """Return a consistently configured project logger."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    return logging.getLogger(name)
