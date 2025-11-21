
---

## 🤝 CONTRIBUTING.md (Detailed Git Flow)

# Contributing to MintCastIQ

We welcome contributors! Please follow these guidelines:

## Workflow
1. Fork and clone the repo:
```bash
git clone https://github.com/MintCastIQ/MintCastIQ.git
cd mintcastiq
```
2. Create a feature branch
```bash
git checkout -b feature/my-feature
```
3. Make changes in one module at a time (sections/, components/, or backend/).
4. Run tests and lint checks:
```bash
npm run lint
pytest
```
5. Commit with clear messages:
```bash
git commit -m "feat: add checklist section"
```
6. Push and open a pull request:
```bash
git push origin feature/my-feature
```
## ## 📦 Pull Requests
- Open a PR against `develop`.
- Include:
  - A summary of changes.
  - Screenshots or demos if UI‑related.
  - Notes on testing and validation.
- Expect review feedback — clarity and reproducibility are prioritized.
---

## 🤝 CONTRIBUTING.md (Contributor onboarding)

```markdown
# Contributing to MintCastIQ

We welcome contributors! Please follow these guidelines:

---
## 👥 Contributor Types (Code)
- **External contributors (not added to repo)**:
  - Fork the repository, make changes, and open pull requests.
  - Can open issues in public repos but cannot be formally assigned to them.
- **Collaborators (added to repo)**:
  - Invited by maintainers via repo settings.
  - Can push branches directly, manage issues, and assign themselves or others.
- **Maintainers**:
  - Review pull requests, merge changes, and manage roadmap alignment.
  - Responsible for enforcing audit‑grade clarity and contributor safety.
---
## Code Standards
- Frontend: React + TypeScript, modular components in /sections and /components.
- Backend: Flask API only, no templates/static.
- Logging: Explicit logging for audit‑grade clarity.
- Naming: Descriptive, contributor‑safe names.

## Git Hygiene
Ignore node_modules/, logs/, webvenv/, __pycache__/.

Tag milestones clearly:
```bash
git tag -a v0.1.0 -m "Initial Vite migration"
git push origin v0.1.0
```
## 🌐 Project Scope
- **Web app**: Primary focus. Built with modern frameworks (React/Vue/Svelte — see README for current stack).
- **Mobile companion**: Planned for later, will reuse web APIs and design principles.
- **Audit‑grade clarity**: Every contribution should be reproducible, documented, and contributor‑safe.
## 🛠 Development Standards
- **Code style**: Follow the linter/formatter rules defined in the repo. Run checks before committing.
- **Documentation**:
  - Update `README.md` if your change affects usage.
  - Add notes to `DEVELOPMENT_GUIDE.md` for architectural or workflow changes.
- **Testing**:
  - Write unit tests for new features.
  - Ensure existing tests pass (`npm test` or equivalent).
---
## 🔒 Contributor Safety
- No secrets, credentials, or personal data in commits.
- Use environment variables for sensitive configs.
- Respect privacy guidelines outlined in `PRIVACY.md`.

## 🚀 Roadmap Alignment
- Contributions should align with the **web‑first roadmap**.
- Mobile features are welcome if scoped as companion modules, not primary focus.
- If unsure, open a **Discussion** or **Issue** before coding.
---
## 🤝 Community Standards
- Be explicit, respectful, and clear in communication.
- Document architectural decisions for future contributors.
- Follow the project’s branding and ergonomic guidelines.
