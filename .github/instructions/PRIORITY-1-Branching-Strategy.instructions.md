---
applyTo: '**'
priority: 1
---
# 🚨 PRIORITY 1: BRANCHING STRATEGY - READ FIRST

## ⚠️ CRITICAL RULES - NEVER VIOLATE THESE:

### 1. NEVER COMMIT DIRECTLY TO MAIN
```bash
# ❌ WRONG - This will be rejected:
git checkout main
git commit -m "some change"
git push origin main
```

### 2. ALWAYS USE FEATURE BRANCHES
```bash
# ✅ CORRECT - Always work on feature branches:
git checkout feature/timesheet-app
git checkout -b feature/timesheet-app/your-specific-feature
# ... make changes ...
git commit -m "feat(timesheet): your change"
git push origin feature/timesheet-app/your-specific-feature
```

### 3. CURRENT ACTIVE BRANCH STRUCTURE
```
main                           # ← Production ready only
├── feature/timesheet-app      # ← Integration branch for timesheet
│   ├── feature/timesheet-app/entry-validation
│   ├── feature/timesheet-app/job-management
│   └── feature/timesheet-app/reporting
├── feature/daycare-invoice    # ← Future integration branch
├── feature/employment-history # ← Future integration branch
└── feature/[other-apps]       # ← Future app branches
```

## 🎯 BRANCH NAMING CONVENTIONS

### For Timesheet Development (Current Focus):
- **App Integration Branch**: `feature/timesheet-app`
- **Specific Features**: `feature/timesheet-app/[feature-name]`

Examples:
```bash
feature/timesheet-app/entry-validation
feature/timesheet-app/job-crud
feature/timesheet-app/time-calculations
feature/timesheet-app/user-interface
feature/timesheet-app/reporting
```

### For Future Apps:
```bash
feature/daycare-invoice/[feature-name]
feature/employment-history/[feature-name]
feature/upcoming-payments/[feature-name]
feature/credit-card-mgmt/[feature-name]
feature/household-budget/[feature-name]
```

## 📋 MANDATORY WORKFLOW SEQUENCE

### 1. Before Starting Any Work:
```bash
# Check current branch
git branch --show-current

# Ensure you're on the right starting point
git checkout feature/timesheet-app  # For timesheet work
git pull origin feature/timesheet-app
```

### 2. Create Feature Branch:
```bash
git checkout -b feature/timesheet-app/your-feature-name
```

### 3. Development Cycle:
```bash
# Test first, commit second
python manage.py check
python manage.py runserver
# Test in browser

# Commit with proper scope
git add .
git commit -m "feat(timesheet): your descriptive message"
```

### 4. Push Feature Branch:
```bash
git push origin feature/timesheet-app/your-feature-name
```

### 5. Merge to Integration Branch:
```bash
git checkout feature/timesheet-app
git merge feature/timesheet-app/your-feature-name
git push origin feature/timesheet-app
```

## 🔄 MERGE FLOW DIAGRAM

```
Developer Feature Branch
       ↓
feature/timesheet-app/specific-feature
       ↓ (merge when ready)
feature/timesheet-app
       ↓ (merge when app complete)
main
```

## ⚡ QUICK COMMANDS

### Start New Feature:
```bash
git checkout feature/timesheet-app
git pull origin feature/timesheet-app
git checkout -b feature/timesheet-app/new-feature
```

### Commit & Push:
```bash
git add .
git commit -m "feat(timesheet): add new functionality"
git push origin feature/timesheet-app/new-feature
```

### Merge to Integration:
```bash
git checkout feature/timesheet-app
git merge feature/timesheet-app/new-feature
git push origin feature/timesheet-app
```

## 🚫 COMMON MISTAKES TO AVOID

1. **Never work directly on `main`**
2. **Never work directly on `feature/timesheet-app`** (create sub-branches)
3. **Never skip testing before committing**
4. **Never use generic commit messages** (use scopes like `feat(timesheet):`)
5. **Never merge incomplete features to integration branch**

## 📍 CURRENT PROJECT STATUS

- **Active Development**: Timesheet app on `feature/timesheet-app`
- **Current Tasks**: Complete timesheet functionality
- **Next Phase**: Integration testing and merge to main
- **Future Work**: Additional apps following same pattern

---

**Remember**: This branching strategy ensures clean, organized development with proper feature isolation and controlled integration. Always follow these rules for consistent, maintainable development workflow.
