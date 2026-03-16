# Security Policy

## Supported Versions

Only the latest commit on the `main` branch is actively maintained.

---

## Secret Scanning & Credential Hygiene

### Never Commit Secrets

Secrets (API keys, tokens, passwords, database connection strings, private certificates) **must never be committed** to this repository.

| Bad ❌ | Good ✅ |
|--------|---------|
| Hard-coded key in source file | Environment variable (`os.environ["MY_KEY"]`) |
| `.env` file committed | `.env` listed in `.gitignore`, values set in CI secrets |
| Token in notebook output | Strip notebook outputs before commit |

### Recommended Workflow

1. Store all secrets in environment variables or a secrets manager.
2. Use a `.env` file locally (never commit it – it is in `.gitignore`).
3. Load variables with `python-dotenv` or your shell's `export` command.
4. In CI/CD, use GitHub Actions [encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

### GitHub Advanced Security

If you have access to GitHub Advanced Security:

* **Secret scanning** automatically alerts maintainers when known secret patterns (API keys, tokens) are pushed. Enable it in *Settings → Security → Secret scanning*.
* **Push protection** blocks pushes containing secrets before they are publicly visible. Enable in *Settings → Security → Push protection*.

---

## What To Do If a Secret Is Leaked

If you accidentally commit a secret, act immediately:

1. **Revoke / rotate the credential** in the issuing service (API console, IAM, etc.) — this is the most important step.
2. Remove the secret from the repository history:
   ```bash
   # Using git-filter-repo (recommended)
   pip install git-filter-repo
   git filter-repo --path <file-with-secret> --invert-paths
   git push --force-with-lease origin main
   ```
3. Notify affected parties if the secret granted access to sensitive systems or data.
4. Open a private GitHub Security Advisory if the leak may have exposed user data.

---

## Reporting a Vulnerability

Please **do not** open a public issue for security vulnerabilities.  
Instead, report them privately via [GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability) or by contacting the repository maintainer directly.

We aim to acknowledge reports within 72 hours and will coordinate a fix and disclosure timeline with you.
