# Contributing to MintCastIQ

MintCastIQ welcomes contributors who value clarity, reproducibility, and audit‑grade workflows. This guide outlines how to collaborate safely and effectively.


## 🧭 Workflow Overview
### 1. Fork and clone the repository
External contributors should fork; collaborators may clone directly.

```bash
git clone https://github.com/MintCastIQ/mintcastiq-web.git
cd mintcastiq-web
```
### 2. Create a feature branch from develop
```bash
git checkout develop
git checkout -b feature/<short-descriptor>
```
Branches should be:
- short‑lived
- purpose‑specific
- named clearly (feature/otp-service, bugfix/session-migration)

### 3. Make focused changes
- Work on one logical unit at a time. 
- Keep changes isolated to a module or service when possible.

### 4. Run tests
All changes must pass the test suite before opening a PR.

```bash
pytest
```
### 5. Commit with clear, contributor‑safe messages
```bash
git commit -m "feat: implement OTP hashing service"
```
### 6. Push and open a pull request
```bash
git push -u origin feature/<short-descriptor>
```
### Open a PR against develop, not main.

## 📦 Pull Request Expectations
Every PR must include:
- Summary of changes
- Reasoning (why this change exists)
- Testing notes (what you validated)
- Screenshots if UI‑related
- Migration notes if schema changes occurred

PRs are reviewed for:
- clarity
- reproducibility
- contributor safety
- architectural alignment

### Expect feedback — this is a forensic‑grade project, not a “just merge it” repo.

## 👥 Contributor Roles
### External Contributors
- Work from forks
- Open PRs to develop
- Can open issues but cannot be assigned to them

### Collaborators
- Added by maintainers
- Can push branches directly
- Can manage issues and self‑assign work

### Maintainers
- Review and merge PRs
- Enforce audit‑grade clarity
- Maintain roadmap alignment
- Ensure contributor safety and documentation quality

## 🧹 Git Hygiene
- Never commit secrets, credentials, or personal data
- Ignore generated or local‑only files:
```Code
node_modules/
logs/
webvenv/
__pycache__/
```
## Tag milestones clearly:

```bash
git tag -a v0.1.0 -m "Initial migration"
git push origin v0.1.0
```
## 🛠 Code & Development Standards
### Code Style
- Prefer explicitness over cleverness
- Use descriptive, contributor‑safe names
- Log intentionally for audit clarity

## Documentation
- Update README.md if usage changes
- Update DEVELOPMENT_GUIDE.md for architectural or workflow changes
- Document new services, models, or ingest behaviors

## Testing
- Add tests for new features
- Ensure all existing tests pass
- Avoid merging untested logic

## 🔒 Contributor Safety
- MintCastIQ is designed to be contributor‑safe and privacy‑respecting.
- Never commit personal data
- Never commit secrets or API keys
- Use environment variables for sensitive configuration
- Follow the guidelines in PRIVACY.md

## 🌐 Project Scope
- Web app: Primary focus (Django + DRF)
- Mobile companion: Planned, but secondary
- Audit‑grade clarity: Every contribution must be reproducible and traceable

## 🚀 Roadmap Alignment
### Before starting major work:
- Open an Issue or Discussion
- Confirm alignment with the web‑first roadmap
- Avoid speculative or unscoped features

## 🤝 Community Standards
- Communicate clearly and respectfully
- Document architectural decisions
- Follow project branding and ergonomic guidelines
- Help maintain a welcoming, contributor‑safe environment