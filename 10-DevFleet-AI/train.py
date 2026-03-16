#!/usr/bin/env python3
"""Training entry point with MLflow and W&B experiment tracking.

Usage
-----
    python scripts/train.py --config configs/example.yaml
    python scripts/train.py --config configs/example.yaml --seed 0
"""

from __future__ import annotations

import argparse
import math
import sys
from collections.abc import Callable
from pathlib import Path

# Allow imports from the project root when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import load_config
from src.utils import enable_deterministic_mode, set_seed


# ---------------------------------------------------------------------------
# Minimal dummy training loop
# ---------------------------------------------------------------------------

def build_dummy_data(n_samples: int = 200, n_features: int = 10) -> tuple[list[list[float]], list[int]]:
    """Generate a trivial random dataset for demonstration purposes."""
    import random

    X = [[random.gauss(0, 1) for _ in range(n_features)] for _ in range(n_samples)]
    y = [random.randint(0, 1) for _ in range(n_samples)]
    return X, y


def train_loop(cfg: dict, run_tracker: Callable[..., None]) -> dict[str, float]:
    """Placeholder training loop that logs synthetic metrics."""
    epochs: int = cfg["training"]["epochs"]
    lr: float = cfg["training"]["learning_rate"]
    metrics: dict[str, float] = {}

    for epoch in range(1, epochs + 1):
        # Synthetic loss curve decaying with a cosine
        loss = 0.5 * (1 + math.cos(math.pi * epoch / epochs)) + 0.05
        acc = 0.5 + 0.5 * (1 - math.cos(math.pi * epoch / epochs))
        metrics = {"loss": round(loss, 4), "accuracy": round(acc, 4)}

        print(f"  Epoch {epoch:>3}/{epochs}  loss={loss:.4f}  acc={acc:.4f}")
        run_tracker(epoch=epoch, **metrics)

    return metrics


# ---------------------------------------------------------------------------
# Experiment tracking helpers
# ---------------------------------------------------------------------------

def setup_mlflow(cfg: dict):
    """Initialise an MLflow run if MLflow tracking is enabled."""
    try:
        import mlflow

        tracking_cfg = cfg.get("tracking", {}).get("mlflow", {})
        if not tracking_cfg.get("enabled", True):
            return None

        uri = tracking_cfg.get("tracking_uri", "./mlruns")
        mlflow.set_tracking_uri(uri)
        mlflow.set_experiment(tracking_cfg.get("experiment_name", "default"))
        run = mlflow.start_run(run_name=cfg["experiment"]["name"])
        mlflow.log_params(
            {
                "seed": cfg["reproducibility"]["seed"],
                "lr": cfg["training"]["learning_rate"],
                "epochs": cfg["training"]["epochs"],
                "batch_size": cfg["training"]["batch_size"],
            }
        )
        print(f"[MLflow] tracking to {uri}  run_id={run.info.run_id}")
        return run
    except ImportError:
        print("[MLflow] not installed – skipping.")
        return None


def setup_wandb(cfg: dict):
    """Initialise a W&B run if W&B tracking is enabled."""
    try:
        import os

        import wandb

        tracking_cfg = cfg.get("tracking", {}).get("wandb", {})
        if not tracking_cfg.get("enabled", False):
            # Ensure offline / disabled so no credentials are needed
            os.environ.setdefault("WANDB_MODE", "disabled")
            return None

        os.environ.setdefault("WANDB_MODE", "offline")
        run = wandb.init(
            project=tracking_cfg.get("project", "ai-research-devfleet"),
            entity=tracking_cfg.get("entity") or None,
            name=cfg["experiment"]["name"],
            config={
                "seed": cfg["reproducibility"]["seed"],
                "lr": cfg["training"]["learning_rate"],
                "epochs": cfg["training"]["epochs"],
                "batch_size": cfg["training"]["batch_size"],
            },
        )
        print(f"[W&B] run initialised (mode={os.environ.get('WANDB_MODE')})")
        return run
    except ImportError:
        print("[W&B] not installed – skipping.")
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Train a model (placeholder).")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/example.yaml"),
        help="Path to YAML config file.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Override the seed in the config file.",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)

    # Override seed from CLI if provided
    if args.seed is not None:
        cfg["reproducibility"]["seed"] = args.seed

    seed: int = cfg["reproducibility"]["seed"]
    print(f"[Seed] {seed}")
    set_seed(seed)
    if cfg["reproducibility"].get("deterministic", True):
        enable_deterministic_mode(
            cudnn_benchmark=cfg["reproducibility"].get("cudnn_benchmark", False)
        )

    # Initialise trackers
    mlflow_run = setup_mlflow(cfg)
    wandb_run = setup_wandb(cfg)

    def log_metrics(epoch: int, **metrics: float) -> None:
        if mlflow_run is not None:
            try:
                import mlflow

                mlflow.log_metrics(metrics, step=epoch)
            except Exception:
                pass
        if wandb_run is not None:
            try:
                wandb_run.log({"epoch": epoch, **metrics})
            except Exception:
                pass

    print(f"\nStarting experiment: {cfg['experiment']['name']}")
    final_metrics = train_loop(cfg, log_metrics)
    print(f"\nFinal metrics: {final_metrics}")

    # Close trackers
    if mlflow_run is not None:
        try:
            import mlflow

            mlflow.log_metrics(final_metrics)
            mlflow.end_run()
        except Exception:
            pass

    if wandb_run is not None:
        try:
            wandb_run.finish()
        except Exception:
            pass


if __name__ == "__main__":
    main()
