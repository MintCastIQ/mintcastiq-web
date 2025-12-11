---
name: Issue Template
about: Describe this issue template's purpose here.
title: ''
labels: ''
assignees: ''

---

# 🧩 Component Issue

## 📖 Summary
Briefly describe the component.  
Example: *Implement reusable header with logo + nav links.*

---

## ✅ Acceptance Criteria
Define what must be true for this issue to be complete:
- Header renders logo and navigation links
- Footer shows copyright and quick links
- Menu highlights active page

---

## 🧪 Testing Steps
How contributors can verify the component works:
1. Run `pytest -q` and confirm all tests pass
2. `curl localhost:8000 | grep "<header>"` shows header markup
3. Navigate to `/about` and confirm menu highlights "About"

---

## 🔗 Dependencies
List any related issues or components this depends on.  
Example: *Depends on #42 (base template)*

---

## 🏷️ Labels
Suggested labels:  
- `component`  
- `good first issue`  
- `frontend`  

---

## 📅 Expected Effort
~1–2 days of development time
