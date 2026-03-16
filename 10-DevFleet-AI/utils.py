"""Reproducibility and general utility helpers.

Usage
-----
    from src.utils import set_seed
    set_seed(42)
"""

from __future__ import annotations

import os
import random


def set_seed(seed: int = 42) -> None:
    """Set random seeds for Python, NumPy, and PyTorch (if available).

    Parameters
    ----------
    seed:
        Integer seed value.  Default is 42.
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    try:
        import numpy as np

        np.random.seed(seed)
    except ImportError:
        pass

    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


def enable_deterministic_mode(cudnn_benchmark: bool = False) -> None:
    """Configure PyTorch for deterministic (reproducible) execution.

    Parameters
    ----------
    cudnn_benchmark:
        When *True*, enables cuDNN auto-tuning for faster convolutions at the
        cost of full determinism.  Defaults to *False*.
    """
    try:
        import torch

        torch.use_deterministic_algorithms(True, warn_only=True)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = cudnn_benchmark
        os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
    except ImportError:
        pass
