#!/usr/bin/env python3
"""Download dataset to the local data/ directory.

Usage
-----
    # Use a URL from the environment variable:
    DATA_URL=https://example.com/dataset.zip python scripts/download_data.py

    # Or run interactively – the script will print instructions:
    python scripts/download_data.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


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
    url = os.environ.get("DATA_URL", "")

    if not url:
        print(
            "No DATA_URL environment variable set.\n\n"
            "Instructions:\n"
            "  1. Set DATA_URL to the URL of your dataset archive.\n"
            "     export DATA_URL=https://example.com/dataset.zip\n"
            "  2. Re-run this script.\n\n"
            f"Downloaded data will be placed in: {DATA_DIR.resolve()}\n"
            "The data/ directory is listed in .gitignore – do NOT commit datasets."
        )
        sys.exit(0)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filename = url.split("/")[-1] or "dataset"
    dest = DATA_DIR / filename
    download(url, dest)


if __name__ == "__main__":
    main()
