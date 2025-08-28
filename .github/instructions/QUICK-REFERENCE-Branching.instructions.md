---
applyTo: 'family-hub-workspace/**'
priority: 'CRITICAL'
---

# 🚨 COPILOT QUICK REFERENCE: FamilyHub Branching

## ⚡ IMMEDIATE ACTIONS REQUIRED

### ✅ BEFORE ANY WORK:
```bash
# 1. Check where you are
pwd
git branch --show-current

# 2. Go to correct app directory  
cd C:/Users/Dmitry/OneDrive/Development/myprojects/family-hub-workspace/standalone-apps/timesheet

# 3. Ensure on app branch (NOT main)
git checkout feature/timesheet-app
git pull origin feature/timesheet-app
```

### 🌿 CREATE NEW FEATURE/FIX:
```bash
# For features:
git checkout -b feature/timesheet-[feature-name]

# For fixes:  
git checkout -b fix/timesheet-[bug-description]

# For docs:
git checkout -b docs/timesheet-[doc-type]
```

### 💾 AFTER CHANGES:
```bash
# Test first!
python manage.py runserver 8001

# Then commit:
git add .
git commit -m "feat(timesheet): descriptive message"
git push origin feature/timesheet-[branch-name]

# Merge to app branch (NOT main):
git checkout feature/timesheet-app
git merge feature/timesheet-[branch-name]
git push origin feature/timesheet-app
```

## 🚨 CRITICAL RULES:

1. **NEVER** create branches from main for app work
2. **NEVER** merge app features directly to main  
3. **ALWAYS** work from app branch: `feature/timesheet-app`
4. **ALWAYS** test before committing
5. **ALWAYS** run commands from correct directory

## 📍 APP DIRECTORIES:
- **Timesheet**: `standalone-apps/timesheet/`
- **Main Project**: `FamilyHub/` 
- **Shared**: `shared/`

## 🎯 CURRENT ACTIVE BRANCHES:
- `main` (production)
- `feature/timesheet-app` (timesheet development)
- `feature/timesheet-template-fixes` (current work)

---
**When in doubt: Branch from app branch, merge back to app branch!**
