#!/usr/bin/env python3
"""Download a pre-trained model to the local models/ directory.

Usage
-----
    # Use a URL from the environment variable:
    MODEL_URL=https://example.com/model.pt python scripts/download_model.py

    # Or run interactively – the script will print instructions:
    python scripts/download_model.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

MODELS_DIR = Path(__file__).parent.parent / "models"


def download(url: str, dest: Path) -> None:
    """Stream-download *url* to *dest*, showing a progress bar."""
    import urllib.request

    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url} → {dest}")

    try:
        from tqdm import tqdm

        class _ProgressHook:
            def __init__(self) -> None:
                self._bar: "tqdm[bytes] | None" = None

            def __call__(self, block_num: int, block_size: int, total_size: int) -> None:
                if self._bar is None:
                    self._bar = tqdm(total=total_size, unit="B", unit_scale=True)
                self._bar.update(block_size)

        hook = _ProgressHook()
        urllib.request.urlretrieve(url, dest, reporthook=hook)
        if hook._bar:
            hook._bar.close()
    except ImportError:
        urllib.request.urlretrieve(url, dest)

    print(f"Saved to {dest}")


def main() -> None:
    url = os.environ.get("MODEL_URL", "")

    if not url:
        print(
            "No MODEL_URL environment variable set.\n\n"
            "Instructions:\n"
            "  1. Set MODEL_URL to the URL of your model weights.\n"
            "     export MODEL_URL=https://example.com/model.pt\n"
            "  2. Re-run this script.\n\n"
            f"Downloaded models will be placed in: {MODELS_DIR.resolve()}\n"
            "The models/ directory is listed in .gitignore – do NOT commit large weight files."
        )
        sys.exit(0)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    filename = url.split("/")[-1] or "model"
    dest = MODELS_DIR / filename
    download(url, dest)


if __name__ == "__main__":
    main()
