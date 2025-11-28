# MintCastIQ Development Guide

## Overview
MintCastIQ is a contributor‑safe pipeline for trading card capture, grading, and benchmarking.  
This guide documents the development environment, contributor workflow, and host worker setup.

---

## Prerequisites
Before starting, ensure the following are installed and configured:

- Docker & Docker Compose
- Git
- Access to `.env` file with Postgres credentials (provided separately)

---

## Clone the Repository
```bash
git clone https://github.com/MintCastIQ/mintcastiq-web.git
```
Install Docker
### Option 1: Quick Install (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install docker.io
sudo systemctl enable --now docker
```
### Option 2: Latest Docker CE & Compose v2 (Recommended)
#### Install prerequisites:
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
```
#### Add Docker’s official GPG key:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
#### Add Docker repo:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
#### Install Docker CE + CLI + Compose plugin:

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
#### Build and Run
```bash
docker compose build --no-cache
docker compose up -d
```
#### Verify Installation
```bash
# Django should respond on port 8000
curl -s http://localhost:8000/ | head -20
```
Expected output: HTML from the Django welcome page.
---

markdown
## Database Connectivity

Run migrations to confirm database connectivity:

```bash
docker compose exec web python backend/manage.py showmigrations
```
### Common Troubleshooting
- ModuleNotFoundError → check spelling in requirements.txt.
- DB connection errors → confirm .env matches your VFM Postgres credentials.
- Static files → ensure BASE_DIR and STATIC_ROOT are defined in settings.py.

### Contributor Workflow
- Primary focus: CPU‑safe development in VMs or local environments.
- Endpoints: Contributors interact with the worker via HTTP API.

### Architecture
- Python and Django
- Docker
- Postgres

### Folder Layout
/opt/mintcastiq-web/ 
├── backend
│   ├── core
│   ├── manage.py
│   ├── mintcastiq
│   │   ├── __pycache__
│   │   └── settings.py
│   └── staticfiles
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── webvenv
### 🌿 Git Branch Naming Policy
To maintain clarity and audit‑grade workflows, all branches must follow these conventions:
- Prefix by Purpose
  - feature/ → new functionality
  - fix/ → bug fixes
  - docs/ → documentation changes
  - test/ → testing or CI improvements
  - chore/ → maintenance, cleanup, dependency bumps
  - hotfix/ → urgent production fixes

- Slug Format
  - Use lowercase words separated by hyphens (-).
  - Keep names short but descriptive (3–5 words).

### Examples
- feature/db-factory-tests
- docs/add-testing-guide
- fix/postgres-uri-validation
### Issue/Ticket Reference
If the branch relates to a GitHub Issue, append the ID:


- feature/db-factory-tests-42
- fix/postgres-uri-validation-17
### Lifecycle Rules
- Branches must be rebased or rebranched if divergence occurs.
- Delete merged branches promptly to avoid stale history.
- Contributors should never push directly to main. Always use a PR workflow.

### Contributor Checklist
✅ Create branch with correct prefix and slug. 
✅ Link branch to issue/ticket in PR description. 
✅ Ensure all tests pass before merge. 
✅ Delete branch after merge.

---

## 📋 Component Tracking

| Component | Status         | Assignee   | Test Coverage | Dependencies      |
|-----------|----------------|------------|---------------|-------------------|
| Header    | 🟡 In Progress | @username  | ✅ Unit tests | Base template     |
| Footer    | 🔵 Not Started | —          | ❌ None       | Base template     |
| Menu/Nav  | 🔵 Not Started | —          | ❌ None       | Context processor |
| Base.html | 🟢 Complete    | @maintainer| ✅ Verified   | —                 |

---

## 🎨 Color Scheme

| Role          | Hex Code | Notes                                      |
|---------------|----------|--------------------------------------------|
| Primary       | #005f73  | Deep teal, strong anchor color             |
| Secondary     | #0a9396  | Bright teal, complements primary           |
| Accent        | #94d2bd  | Soft aqua, good for highlights             |
| Background    | #e9d8a6  | Warm sand, easy on the eyes                |
| Highlight     | #ee9b00  | Amber, draws attention without glare       |
| Alert/Warning | #ca6702  | Burnt orange, readable on light/dark       |
| Success       | #2a9d8f  | Green-blue, safe for colorblind users      |
| Neutral Dark  | #001219  | Near black, high contrast text             |
| Neutral Mid   | #7d8597  | Muted gray, for secondary text             |
| Neutral Light | #fefefe  | White, clean background                    |

---

## 🧩 MintCastIQ Docstring Style Guide

### 🔹 General Format
```text
"""
[One-line summary]
[Extended description if needed — what the function/class does, why it matters, and any contributor notes.]
Args:
    arg1 (type): Description of the argument and its role in validation or logic.
    arg2 (type): Description of the argument.
Returns:
    type: Description of the return value and its structure.
Raises:
    ExceptionType: Conditions under which this exception is raised.
Example:
    >>> result = function_name("input")
    >>> assert result == expected_output
"""
```
### 🧪 Example: Validator Function
```python
def validate_slug(value):
    """
    Validates that a slug contains only lowercase letters, numbers, and hyphens.
    Ensures audit-safe identifiers for DimCard objects and prevents ambiguity in hash tracking.

    Args:
        value (str): The slug string to validate.
    Raises:
        ValidationError: If the slug contains invalid characters.
    Example:
        >>> validate_slug("mintcastiq-2025")
    """
```
### 🧬 Example: Model Method (clean)
```python
def clean(self):
    """
    Validates cross-field integrity for DimCard objects.
    Ensures that `hash_count` is exactly 10, enforcing forensic consistency.

    Raises:
        ValidationError: If `hash_count` is not equal to 10.
    """
```
### 🧱 Example: Class-Level Docstring
```python
class DimCard(models.Model):
    """
    Represents a validated trading card within the MintCastIQ system.
    Each card must store exactly 10 hashes for forensic deduplication and contributor-safe onboarding.
    """
```
## 🗑️ Soft Delete and Status Enum
We use a soft delete pattern to ensure records are never physically removed. Instead, each model that inherits from SoftDeleteMixin has a status field:
- Status.ACTIVE → record is live and queryable
- Status.INACTIVE → record is soft‑deleted but still present for audit purposes

### Managers
```python
objects  # returns all records (active + inactive)
active   # returns only active records
```
#### Example Usage
```python
from app.models import YourModel

# Create (defaults to active)
obj = YourModel.objects.create(name="Example")

# Soft delete
obj.soft_delete()
assert obj.status == Status.INACTIVE

# Restore
obj.restore()
assert obj.status == Status.ACTIVE

# Query sets
YourModel.objects.all()    # includes inactive rows
YourModel.active.all()     # only active rows
```
## 🧮 Hash Run Integrity Checklist
Each card image produces 10 positional hashes grouped by hash_run. The hash_run column starts at 1 for the first image of a card and increments by 1 for each new image.

### Model Constraint
```python
class DimCardHash(models.Model):
    card = models.ForeignKey("Card", on_delete=models.CASCADE)
    hash_position = models.CharField(max_length=20, choices=HashPosition.choices)
    hash_value = models.CharField(max_length=64, db_index=True)
    hash_run = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["card", "hash_run", "hash_position"],
                name="unique_card_run_position"
            )
        ]
```
### Verify Integrity
```bash
python manage.py shell -c "
from app.models import DimCardHash, Card;
card = Card.objects.first();
for run in DimCardHash.objects.filter(card=card).values_list('hash_run', flat=True).distinct():
    count = DimCardHash.objects.filter(card=card, hash_run=run).count()
    print(f'Card {card.id}, run {run}: {count} positions')"
```
### Insert Example
```Python
from django.db import models
from app.models import DimCardHash, Card, HashPosition
card = Card.objects.first()
last_run = DimCardHash.objects.filter(card=card).aggregate(
    models.Max("hash_run")
)["hash_run__max"] or 0
new_run = last_run + 1

for pos in HashPosition.values:
    DimCardHash.objects.create(
        card=card,
        hash_position=pos,
        hash_value="demo_hash",
        hash_run=new_run
    )
```
## 🎴 Parallels: Abstract vs. Concrete
Parallels exist at two levels:
- Abstract (Set‑level definition)
  - Each set defines its own list of parallels (e.g., "Rainbow Foil", "Diamante").
  - Persisted once per set in DimParallel.
  - Example: 2025 Topps Baseball → Diamante.
- Concrete (Card‑level inventory)
  - Linked to a card only when inventory confirms it exists.
  - Persisted in DimCardParallel.
  - Example: Card #12345 → Diamante.

### Schema Relationships
DimSet
 └── DimParallel (abstract definitions per set)
      └── DimCardParallel (concrete inventory links)
           └── DimCard (actual card objects)
- DimParallel: Defines all parallels for a set, even if none are inventoried yet.
- DimCardParallel: Links a card to a parallel only when inventory confirms it.
- DimCard: The card object itself, independent of parallels.

### Contributor Checklist
Verify defined parallels for a set

```bash
python manage.py shell -c "
from app.models import DimParallel, DimSet;
set = DimSet.objects.get(name='2025 Topps Baseball');
print('Defined parallels:', list(DimParallel.objects.filter(set=set).values_list('name', flat=True)))"
```
### Verify inventory parallels for a card

```bash
python manage.py shell -c "
from app.models import DimCardParallel, Card;
card = Card.objects.first();
print('Inventory parallels:', list(DimCardParallel.objects.filter(card=card).values_list('parallel__name', flat=True)))"
```
### Verify both set and card together

```bash
python manage.py shell -c "
from app.models import DimParallel, DimCardParallel, DimSet, Card;
set = DimSet.objects.get(name='2025 Topps Baseball');
print('Defined parallels for set:', list(DimParallel.objects.filter(set=set).values_list('name', flat=True)));

card = Card.objects.first();
print('Inventory parallels for card:', list(DimCardParallel.objects.filter(card=card).values_list('parallel__name', flat=True)));"
```
## 🔐 Best Practices
- Always include runnable examples — contributors can copy/paste and test instantly.
- Explain why — not just what the function does, but why it matters to MintCastIQ’s integrity.
- Use consistent phrasing — e.g., “forensic validation”, “contributor‑safe”, “audit‑grade”.





