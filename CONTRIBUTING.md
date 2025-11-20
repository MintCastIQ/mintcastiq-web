# Contributing to MintCastIQ
- Thank you for your interest in contributing!  
MintCastIQ is evolving into a **web‑first platform** with a mobile companion planned down the road. This guide outlines how to participate safely, effectively, and in line with our audit‑grade standards.
---
## 🧩 Getting Started
- **Fork the repo** and create a feature branch:
  ```bash
  git checkout -b feature/my-feature
  ```
- Keep commits atomic — one logical change per commit.
- Write clear commit messages:
- Use imperative mood (“Add overlay pipeline”).
- Reference issues when applicable (Fixes #42).
---
## Contributor Roles

MintCastIQ supports two primary contributor types:

### 1. Code Contributors
- **Focus:** Application logic, infrastructure, and pipeline improvements.
- **Access:** Git repository, issue tracker, and development environment.
- **Responsibilities:**
  - Implement new features and bug fixes.
  - Maintain audit‑grade commit hygiene (tags, milestones, documentation).
  - Respect modular architecture and contributor‑safe onboarding practices.
  - Document architectural decisions in `DEVELOPMENT_GUIDE.md`.

### 2. Scan Contributors
- **Focus:** Providing card scans for probabilistic grading and forensic validation.
- **Access:** Upload endpoints, contributor‑safe capture pipeline, and annotation guides.
- **Responsibilities:**
  - Follow capture standards (lighting, orientation, resolution).
  - Ensure each card submission includes exactly 10 hashes for deduplication.
  - Use ergonomic UI and symbolic overlays (no autoscan defaults).
  - Respect contributor‑safe storage practices (symlinked pipelines, audit‑grade rotation).

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
## 📦 Pull Requests
- Open a PR against `develop`.
- Include:
  - A summary of changes.
  - Screenshots or demos if UI‑related.
  - Notes on testing and validation.
- Expect review feedback — clarity and reproducibility are prioritized.
---
## 🚀 Roadmap Alignment
- Contributions should align with the **web‑first roadmap**.
- Mobile features are welcome if scoped as companion modules, not primary focus.
- If unsure, open a **Discussion** or **Issue** before coding.
---
## 🤝 Community Standards
- Be explicit, respectful, and clear in communication.
- Document architectural decisions for future contributors.
- Follow the project’s branding and ergonomic guidelines.
