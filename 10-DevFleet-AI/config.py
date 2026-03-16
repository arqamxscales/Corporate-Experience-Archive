"""Configuration loading utilities.

Usage
-----
    from src.config import load_config
    cfg = load_config("configs/example.yaml")
    print(cfg["experiment"]["name"])
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file and resolve environment-variable overrides.

    Parameters
    ----------
    path:
        Path to the YAML config file.

    Returns
    -------
    dict
        Parsed configuration dictionary.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r") as fh:
        cfg: dict[str, Any] = yaml.safe_load(fh) or {}

    # Allow environment variables to override tracking URIs / keys
    if "tracking" in cfg:
        mlflow_cfg = cfg["tracking"].get("mlflow", {})
        if "MLFLOW_TRACKING_URI" in os.environ:
            mlflow_cfg["tracking_uri"] = os.environ["MLFLOW_TRACKING_URI"]

        wandb_cfg = cfg["tracking"].get("wandb", {})
        wandb_mode = os.environ.get("WANDB_MODE", "")
        if wandb_mode.lower() == "online":
            wandb_cfg["enabled"] = True
        elif wandb_mode.lower() == "disabled":
            wandb_cfg["enabled"] = False

    return cfg
