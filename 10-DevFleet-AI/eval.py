#!/usr/bin/env python3
"""Evaluation entry point – reads model artefacts and reports metrics.

Usage
-----
    python scripts/eval.py --config configs/example.yaml --checkpoint models/best.ckpt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow imports from the project root when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import load_config
from src.utils import set_seed


def evaluate(cfg: dict, checkpoint: Path | None) -> dict[str, float]:
    """Placeholder evaluation routine.

    Replace this function with your real evaluation logic.

    Parameters
    ----------
    cfg:
        Loaded configuration dictionary.
    checkpoint:
        Optional path to a saved model checkpoint.

    Returns
    -------
    dict
        Dictionary of metric names to values.
    """
    if checkpoint is not None:
        if not checkpoint.exists():
            print(f"[Warning] Checkpoint not found: {checkpoint}")
        else:
            print(f"[Eval] Loading checkpoint from {checkpoint}")

    # Placeholder metrics
    metrics = {"test_loss": 0.1234, "test_accuracy": 0.9512}
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained model (placeholder).")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/example.yaml"),
        help="Path to YAML config file.",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=None,
        help="Path to model checkpoint (e.g., models/best.ckpt).",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    set_seed(cfg["reproducibility"]["seed"])

    print(f"Evaluating experiment: {cfg['experiment']['name']}")
    metrics = evaluate(cfg, args.checkpoint)

    print("\nEvaluation results:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")


if __name__ == "__main__":
    main()
