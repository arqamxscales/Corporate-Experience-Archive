# Contributing to AI-Research-DevFleet

Thank you for your interest in contributing! This document explains how to set up your environment, submit changes, and follow project conventions.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Branching Strategy](#branching-strategy)
3. [Commit Messages](#commit-messages)
4. [Code Style](#code-style)
5. [Running Checks](#running-checks)
6. [Submitting a Pull Request](#submitting-a-pull-request)
7. [Reporting Bugs / Requesting Features](#reporting-bugs--requesting-features)

---

## Getting Started

### Prerequisites

* Python ≥ 3.10
* `git`
* (Optional) C/C++ toolchain for the `cpp/` components

### Installation

```bash
# 1. Fork and clone
git clone https://github.com/<your-username>/AI-Research-DevFleet.git
cd AI-Research-DevFleet

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3a. Install via requirements.txt (basic)
pip install -r requirements.txt

# 3b. OR install as an editable package (recommended for development)
pip install -e ".[dev]"
```

### Environment Variables

Copy `.env.example` (if present) to `.env` and fill in your values.  
**Never commit the `.env` file** – it is listed in `.gitignore`.

---

## Branching Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable, production-ready code |
| `feature/<short-name>` | New features |
| `fix/<short-name>` | Bug fixes |
| `docs/<short-name>` | Documentation-only changes |
| `experiment/<short-name>` | Exploratory experiments (may be merged or discarded) |

Always branch off `main` unless you are stacking changes on an existing PR.

---

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<optional scope>): <short summary>

[optional body]

[optional footer(s)]
```

Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`.

Examples:

```
feat(train): add cosine LR scheduler support
fix(config): handle missing YAML key gracefully
docs(readme): add experiment tracking section
```

---

## Code Style

* **Python**: formatted with [Black](https://black.readthedocs.io/) (`line-length = 88`) and linted with [Ruff](https://docs.astral.sh/ruff/).
* **Type hints**: encouraged for all public functions.
* **Docstrings**: NumPy or Google style.
* **C/C++**: follow the project's `clang-format` configuration (if present).

---

## Running Checks

```bash
# Format code
black .

# Lint
ruff check .

# Type-check (optional)
mypy src/

# Syntax check all Python files
python -m compileall src/ scripts/

# Run tests (if present)
pytest
```

---

## Submitting a Pull Request

1. Ensure your branch is up to date with `main`.
2. Run all checks listed above and fix any errors.
3. Push your branch and open a PR against `main`.
4. Fill in the PR template (description, motivation, testing notes).
5. Request a review from a maintainer.

PRs that change experiment configs or add new dependencies must update `requirements.txt` **and** `pyproject.toml` accordingly.

---

## Reporting Bugs / Requesting Features

Open a GitHub Issue using one of the provided templates. Please include:

* A clear description of the problem or request.
* Steps to reproduce (for bugs).
* Expected vs. actual behavior.
* Environment details (`python --version`, OS, GPU if relevant).
