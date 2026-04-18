# Week 3 — CI/CD Using GitHub Actions

## Student Details
- Name: MOHAMMAD ARQAM JAVED

This project completes the Week 3 hands-on tasks with a Python app, tests, GitHub Actions workflow, and optional Docker image build/push.

## 1) What is CI?
`CI` (Continuous Integration) means code is pushed frequently, and each push is automatically built and tested so issues are caught early.

## 2) What is CD?
`CD` means:
- Continuous Delivery: app is always ready to deploy.
- Continuous Deployment: app is deployed automatically after passing pipeline checks.

## 3) How GitHub Actions works
Workflow file: [ .github/workflows/ci.yml ](.github/workflows/ci.yml)
- Trigger: `push`, `pull_request`, `workflow_dispatch`
- Job 1: build + test Python app
- Job 2: optional Docker build + push (only on `main` and only if Docker secrets exist)

## 4) Run locally
1. Install deps:
   - `pip install -r requirements.txt`
2. Run app:
   - `python app.py`
3. Run tests:
   - `pytest -v`

## 5) Docker secrets required (for optional job)
Add in GitHub repo:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

Location: **Settings → Secrets and variables → Actions**

## 6) Architecture diagram (you can screenshot this)
```mermaid
flowchart LR
  Dev[Developer] -->|git push / PR| GH[GitHub Repository]
  GH -->|Trigger| WF[GitHub Actions Workflow]
  WF --> R[GitHub Runner]
  R --> B[Build Job]
  B --> T[Test Job]
  T --> D[Docker Build & Push (Optional)]
  D --> DH[Docker Hub]
  T --> DEP[Deployment Target (Optional)]
```

## 7) Submission checklist (single PDF)
- Screenshot of passing GitHub workflow
- Screenshot of test results
- Screenshot of Docker Hub image (if used)
- Architecture diagram
- Short explanation of `CI`, `CD`, and GitHub Actions flow
