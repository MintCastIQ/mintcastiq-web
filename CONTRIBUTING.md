
---

## 🤝 CONTRIBUTING.md (Contributor onboarding)

```markdown
# Contributing to MintCastIQ

We welcome contributors! Please follow these guidelines:

## Workflow
1. Fork and clone the repo.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Make changes in **one module at a time** (`sections/`, `components/`, or `backend/`).
4. Run tests and lint checks.
5. Commit with clear messages.
6. Submit a pull request.

## Code Standards
- **Frontend**: React + TypeScript, modular components in `/sections` and `/components`.
- **Backend**: Flask API only, no templates/static.
- **Logging**: Explicit logging for audit‑grade clarity.
- **Naming**: Descriptive, contributor‑safe names.

## Node & Python Versions
- Node ≥ 20.20.0 (or 21.x)
- Python 3.12

## Git Hygiene
- Ignore `node_modules/`, `logs/`, `webvenv/`, `__pycache__/`.
- Tag milestones clearly.
