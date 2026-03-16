# AI-Research-DevFleet

> Reproducible AI research utilities developed during the **DevFleet Technologies** internship (Jan 5 – Jan 30, 2026).

---

## Table of Contents

1. [Overview](#overview)
2. [Repository Architecture](#repository-architecture)
3. [Quickstart](#quickstart)
4. [Running Scripts](#running-scripts)
5. [Reproducibility](#reproducibility)
6. [Experiment Tracking](#experiment-tracking)
7. [Dataset & Model Downloads](#dataset--model-downloads)
8. [Notebooks](#notebooks)
9. [C/C++ Components](#cc-components)
10. [Reports](#reports)
11. [Contributing & Community](#contributing--community)

---

## Overview

This repository contains the research artefacts, experiment configs, and utility code produced during an AI research internship at **DevFleet Technologies**.  Key areas covered:

- **Data Analysis** – exploratory analysis to support model development.
- **Model Development** – training pipelines for AI-based solutions.
- **Evaluation** – benchmarking and evaluation of AI architectures.

All experiments are **config-driven** and **seed-reproducible**, with first-class support for [MLflow](https://mlflow.org) and [Weights & Biases](https://wandb.ai) experiment tracking.

---

## Repository Architecture

```
AI-Research-DevFleet/
├── configs/            # YAML experiment configurations
│   └── example.yaml
├── cpp/                # Optional C/C++ components
│   ├── CMakeLists.txt
│   └── src/
├── data/               # Datasets (git-ignored – see data/README.md)
├── models/             # Saved checkpoints (git-ignored)
├── notebooks/          # Exploratory Jupyter notebooks
├── reports/            # Research reports and deliverables
├── runs/               # Local training runs / TensorBoard logs (git-ignored)
├── scripts/            # Runnable entry-point scripts
│   ├── download_data.py
│   ├── download_model.py
│   ├── train.py
│   └── eval.py
├── src/                # Importable Python package
│   ├── __init__.py
│   ├── config.py       # YAML config loader with env-var overrides
│   └── utils.py        # Seed setting & determinism helpers
├── .github/
│   └── dependabot.yml
├── pyproject.toml
├── requirements.txt
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
└── SECURITY.md
```

---

## Quickstart

### Prerequisites

- Python ≥ 3.10
- `git`
- (Optional) A CUDA-capable GPU for accelerated training

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/arqamxjay/AI-Research-DevFleet.git
cd AI-Research-DevFleet

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3a. Install dependencies via requirements.txt
pip install -r requirements.txt

# 3b. OR install as an editable package (recommended for development)
pip install -e .                  # core only
pip install -e ".[tracking]"      # + MLflow & W&B
pip install -e ".[dev]"           # + dev tools (black, ruff, pytest …)
```

### Run a sample training job

```bash
python scripts/train.py --config configs/example.yaml
```

You should see per-epoch loss/accuracy output and a local `mlruns/` directory created by MLflow.

---

## Running Scripts

| Script | Purpose | Example |
|--------|---------|---------|
| `scripts/train.py` | Train a model | `python scripts/train.py --config configs/example.yaml --seed 0` |
| `scripts/eval.py` | Evaluate a checkpoint | `python scripts/eval.py --config configs/example.yaml --checkpoint models/best.ckpt` |
| `scripts/download_data.py` | Fetch dataset | `DATA_URL=https://… python scripts/download_data.py` |
| `scripts/download_model.py` | Fetch pretrained weights | `MODEL_URL=https://… python scripts/download_model.py` |

---

## Reproducibility

All experiments are fully config-driven. To reproduce a run:

1. **Use the same config file** (`configs/example.yaml` or a copy of it).
2. **Set the same seed** (`reproducibility.seed` in the YAML, or `--seed <n>` on the CLI).
3. **Enable deterministic mode** (`reproducibility.deterministic: true`) – this sets Python, NumPy, and PyTorch seeds and configures cuDNN for deterministic execution.

```yaml
# configs/example.yaml (excerpt)
reproducibility:
  seed: 42
  deterministic: true
  cudnn_benchmark: false   # false = fully deterministic; true = faster convolutions
```

Determinism utilities live in `src/utils.py`:

```python
from src.utils import set_seed, enable_deterministic_mode

set_seed(42)
enable_deterministic_mode()
```

---

## Experiment Tracking

### MLflow (default – no credentials required)

MLflow is enabled by default and writes runs to a local `./mlruns/` directory.

```bash
# Run training (MLflow logs automatically)
python scripts/train.py --config configs/example.yaml

# Launch the MLflow UI
mlflow ui --backend-store-uri ./mlruns
# Open http://localhost:5000
```

To use a remote tracking server, set the environment variable:

```bash
export MLFLOW_TRACKING_URI=https://your-mlflow-server
```

Disable MLflow by setting `tracking.mlflow.enabled: false` in your config.

### Weights & Biases (offline by default)

W&B is **disabled** by default. Enable it in three ways:

```bash
# 1. Set WANDB_MODE=online (requires W&B account + API key)
export WANDB_MODE=online
export WANDB_API_KEY=your_key_here   # never commit this!
python scripts/train.py --config configs/example.yaml

# 2. Enable offline mode (logs locally, sync later)
export WANDB_MODE=offline
python scripts/train.py ...
wandb sync wandb/

# 3. Enable in the config file
# tracking.wandb.enabled: true
```

> **Security**: never hard-code API keys. Use environment variables or a `.env` file (which is git-ignored). See `SECURITY.md` for details.

---

## Dataset & Model Downloads

```bash
# Download dataset
export DATA_URL=https://example.com/dataset.zip
python scripts/download_data.py

# Download pretrained model
export MODEL_URL=https://example.com/model.pt
python scripts/download_model.py
```

Downloaded files are placed in `data/` and `models/` respectively – both directories are git-ignored. See `data/README.md` for the expected directory layout.

---

## Notebooks

Exploratory notebooks live in `notebooks/`. See `notebooks/README.md` for the full policy.  Key rules:

- **Clear outputs** before committing.
- **No business logic** in notebooks – import from `src/` instead.
- Convert mature notebooks to scripts using `jupyter nbconvert --to script`.

---

## C/C++ Components

A minimal CMake scaffold is provided in `cpp/`:

```bash
mkdir -p cpp/build && cd cpp/build
cmake ..
cmake --build . --parallel
./cpp_placeholder
```

Replace `cpp/src/placeholder.cpp` with your implementation. Build artefacts are git-ignored.

---

## Reports

Research reports produced during the internship are stored in `reports/`:

| File | Description |
|------|-------------|
| `reports/Report` | General internship research report |
| `reports/Model Evaluation Report` | Model evaluation findings |
| `reports/Model Deployment Report` | Model deployment findings |

---

## Contributing & Community

- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, branching, style, and PR guidelines.
- **Code of Conduct**: See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- **Security / Secret scanning**: See [SECURITY.md](SECURITY.md).
- **Dependency updates**: Automated weekly via [Dependabot](.github/dependabot.yml).

---

*Internship completed under the supervision of **Farhan Sohail Khan (CEO), DevFleet Technologies**.*
