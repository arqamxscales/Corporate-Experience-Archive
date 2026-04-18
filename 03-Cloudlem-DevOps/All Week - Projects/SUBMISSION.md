# WEEK 3 CI/CD SUBMISSION

**Student Name:** MOHAMMAD ARQAM JAVED

**Date:** April 10, 2026

**Repository:** https://github.com/arqamxscales/Cloudlem-Week3-Assignment

**Latest Passing Run:** https://github.com/arqamxscales/Cloudlem-Week3-Assignment/actions/runs/24244931330

---

## 1. WHAT IS CI? (Continuous Integration)

**CI (Continuous Integration)** is a software development practice where developers frequently push code to a shared repository. Each push triggers:

- **Automatic builds** of the entire application
- **Automated tests** to validate code quality
- **Early issue detection** to catch problems before they reach production
- **Continuous stability** ensuring the main branch is always production-ready

**Key Benefits:**
- Reduces integration bugs
- Accelerates bug fixes
- Improves code quality
- Shortens development cycles

---

## 2. WHAT IS CD? (Continuous Deployment)

**CD has two interpretations:**

### Continuous Delivery
- Code changes are automatically prepared and validated for production
- Release requires manual approval
- Ensures deployment readiness at all times

### Continuous Deployment
- Code changes are automatically deployed to production after passing pipeline checks
- No manual approval step required
- Fastest delivery cycle

**Key Benefits:**
- Faster releases to end users
- Reduced human error in deployments
- Consistent, repeatable deployment process
- Easy rollback with version history

---

## 3. HOW GITHUB ACTIONS WORKS

### Overview
GitHub Actions is a CI/CD system integrated directly into GitHub. It automates workflows on predefined triggers.

### Workflow Components

**Triggers:** When the workflow runs
- `push` - on code push to specified branches
- `pull_request` - on PR creation/update
- `workflow_dispatch` - manual trigger
- `schedule` - timed/cron-based

**Jobs:** Sets of tasks executed in parallel or sequence
- Each job runs in its own runner
- Can have dependencies (need: job-name)

**Steps:** Individual commands within a job
- Uses GitHub actions (pre-built tasks)
- Runs shell commands
- Sequential execution

**Runners:** Virtual machines that execute workflows
- Ubuntu (Linux)
- Windows
- macOS
- Self-hosted

### Our Week 3 Workflow

**File Location:** `.github/workflows/ci.yml`

**Jobs:**
1. **test-app** (runs on every push/PR)
   - Checkout code
   - Setup Python 3.10
   - Install dependencies (pytest)
   - Run tests with pytest

2. **docker-build-push** (optional, runs on main branch only)
   - Depends on test-app passing
   - Logs into Docker Hub
   - Builds Docker image
   - Pushes image to Docker Hub

---

## 4. PROJECT STRUCTURE

```
Week 3/
├── app.py                    # Main Python application
├── test_app.py              # Test suite
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── index.html              # Static HTML for deployment
├── README.md               # Project documentation
├── SUBMISSION.md           # This file
└── .github/
    └── workflows/
        └── ci.yml          # GitHub Actions workflow
```

---

## 5. ARCHITECTURE DIAGRAM

```
┌─────────────┐
│  Developer  │
└──────┬──────┘
       │ git push / PR
       ▼
┌──────────────────────┐
│ GitHub Repository    │
└──────┬───────────────┘
       │ Trigger Event
       ▼
┌──────────────────────┐
│ GitHub Actions       │
│ (ci.yml workflow)    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Ubuntu Runner        │
└──────┬───────────────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌──────┐ ┌──────────┐
│Build │ │Run Tests │
└──┬───┘ └────┬─────┘
   │          │
   └────┬─────┘
        │ (Tests Pass)
        ▼
┌─────────────────────────┐
│ Docker Build & Push     │
│ (Optional, on main)     │
└──────┬──────────────────┘
       │
       ▼
┌──────────────────┐
│  Docker Hub      │
│ (Image Registry) │
└──────────────────┘
```

---

## 6. TEST RESULTS

**Local Test Execution:**

```
============================= test session starts ==============================
platform darwin -- Python 3.14.3, pytest-8.3.5, pluggy-1.6.0
collected 2 items

test_app.py::test_sample PASSED                                          [ 50%]
test_app.py::test_app_runs PASSED                                        [100%]

============================== 2 passed in 0.01s ===============================
```

**Tests Included:**
- `test_sample()` - Basic assertion (1 + 1 = 2)
- `test_app_runs()` - Validates app returns expected string

---

## 7. SUBMISSION CHECKLIST

To complete your Week 3 submission:

- [x] Push this project to GitHub (main branch)
- [x] Wait for GitHub Actions workflow to complete
- [x] **Take Screenshot #1:** GitHub Actions workflow status (passing)
- [x] **Take Screenshot #2:** Test job results from workflow run
- [x] (Optional Docker job handled) Workflow shows Docker step as optional and skipped when secrets are not configured
- [ ] (Optional, only if required by instructor) Add Docker Hub screenshot
- [x] **Screenshot #4:** Architecture diagram (use the mermaid diagram above or create your own)
- [ ] Compile all screenshots + this document into single PDF
- [ ] Submit PDF to course platform

---

## 8. SCREENSHOT EVIDENCE (ATTACHED)

Below are the screenshots captured for grading:

1. **Workflow Summary (Success)**
       - Shows pipeline passed with status **Success**
       - Run link: https://github.com/arqamxscales/Cloudlem-Week3-Assignment/actions/runs/24244931330

2. **Build and Test Job Details**
       - Shows steps including setup, dependency install, and test execution

3. **Docker Build and Push (Optional) Job Details**
       - Shows optional Docker job completed with skip logic when Docker secrets are not set
       - This is acceptable for optional Docker part unless instructor explicitly requires Docker Hub publish

4. **Pipeline Graph / Flow View**
       - Shows job dependency flow in GitHub Actions UI

> Note: GitHub Actions displays a warning annotation for deprecated Node.js 20 actions in some reusable actions. This does **not** fail the workflow and does not affect pass status for this assignment.

---

## 9. QUICK START FOR GITHUB PUSH

```bash
# Already completed for this submission
git add .
git commit -m "Finalize Week 3 submission details"
git push
```

Actions tab: `https://github.com/arqamxscales/Cloudlem-Week3-Assignment/actions`

---

## 10. DOCKER SECRETS SETUP (Optional)

If you want the Docker build & push job to run:

1. Go to your GitHub repo → **Settings**
2. Click **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add:
   - Name: `DOCKER_USERNAME` → Value: your Docker Hub username
   - Name: `DOCKER_PASSWORD` → Value: your Docker Hub password or token
5. Rerun the workflow

---

## 11. KEY LEARNING OUTCOMES

✅ Understand CI/CD principles and their importance in DevOps

✅ Create and configure GitHub Actions workflows

✅ Automate testing in CI pipelines

✅ Build and push Docker images via CI/CD

✅ Deploy applications reliably and consistently

---

**Project Complete!** 🚀

For questions, refer to [README.md](README.md) or GitHub Actions documentation.
