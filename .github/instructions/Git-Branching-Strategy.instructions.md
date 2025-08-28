---
applyTo: 'family-hub-workspace/**'
---

# FamilyHub Project: Git Branching Strategy & Copilot Instructions

## 🎯 CRITICAL: Always Follow This Branching Strategy

### 📋 Branch Hierarchy (MANDATORY)
```
main (production-ready code only)
├── feature/timesheet-app (long-running app development)
│   ├── feature/timesheet-[specific-feature] (individual features)
│   ├── fix/timesheet-[bug-description] (bug fixes within app)
│   └── docs/timesheet-[documentation] (documentation updates)
├── feature/daycare-invoice-app (another app)
├── feature/employment-history-app (another app)
└── hotfix/[critical-issue] (urgent fixes to main)
```

## ⚠️ NEVER COMMIT DIRECTLY TO MAIN BRANCH

### 🔄 Mandatory Workflow Process

#### For New Features or Bug Fixes:
1. **ALWAYS start from the app branch, NOT main**
   ```bash
   git checkout feature/[app-name]-app
   git pull origin feature/[app-name]-app
   git checkout -b feature/[app-name]-[feature-name]
   ```

2. **Work on your feature/fix**
   - Make changes
   - Test thoroughly  
   - Commit with descriptive messages

3. **Push feature branch**
   ```bash
   git push origin feature/[app-name]-[feature-name]
   ```

4. **Merge back to app branch (NOT main)**
   ```bash
   git checkout feature/[app-name]-app
   git merge feature/[app-name]-[feature-name]
   git push origin feature/[app-name]-app
   ```

5. **Clean up feature branch**
   ```bash
   git branch -d feature/[app-name]-[feature-name]
   git push origin --delete feature/[app-name]-[feature-name]
   ```

#### For App Completion (ONLY when entire app is ready):
```bash
git checkout main
git pull origin main
git merge feature/[app-name]-app
git push origin main
```

### 🎨 Branch Naming Conventions

#### App-Level Branches:
- `feature/timesheet-app` - Main timesheet application
- `feature/daycare-invoice-app` - Daycare invoice tracker
- `feature/employment-history-app` - Employment history tracker

#### Feature/Fix Branches (within apps):
- `feature/timesheet-validation` - Add validation to timesheet
- `feature/timesheet-reporting` - Add reporting features
- `fix/timesheet-template-error` - Fix template syntax issues
- `docs/timesheet-api` - Document timesheet API

#### Emergency Fixes:
- `hotfix/security-vulnerability` - Critical security fix
- `hotfix/production-crash` - Emergency production fix

### 🚨 Copilot Development Rules

#### BEFORE Starting Any Work:
1. **Check current branch**: Ensure you're on the correct app branch
2. **Pull latest changes**: Always sync with remote before creating new branches
3. **Verify branch hierarchy**: Confirm you're branching from app branch, not main

#### DURING Development:
1. **Test frequently**: Run server and verify changes work
2. **Commit regularly**: Small, focused commits with good messages
3. **Follow naming conventions**: Use proper prefixes (feature/, fix/, docs/)

#### AFTER Completing Work:
1. **Test thoroughly**: Ensure all functionality works
2. **Merge to app branch**: Never merge directly to main
3. **Clean up**: Delete feature branches after successful merge

### 📝 Commit Message Standards

#### Format:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

#### Examples:
```bash
# Feature commits
feat(timesheet): add job management CRUD operations
feat(timesheet): implement time entry validation
feat(timesheet): add weekly summary dashboard

# Bug fixes
fix(timesheet): resolve template syntax error in job_list.html
fix(timesheet): correct timezone handling in calculations
fix(timesheet): prevent duplicate time entries

# Documentation
docs(timesheet): add development workflow instructions
docs(timesheet): update API documentation

# Refactoring
refactor(timesheet): simplify time calculation logic
refactor(timesheet): optimize database queries

# Tests
test(timesheet): add unit tests for time entry model
test(timesheet): add integration tests for job management
```

### 🛠️ Development Environment Setup

#### Required Directory Structure:
```
family-hub-workspace/
├── FamilyHub/ (main integrated project)
├── standalone-apps/ (individual apps)
│   ├── timesheet/
│   ├── daycare_invoice/
│   └── ...
└── shared/ (shared components)
```

#### Always Work From Correct Directory:
- **Timesheet App**: `standalone-apps/timesheet/`
- **Main Project**: `FamilyHub/`
- **Commands Must Be Run From App Directory**

### 🚀 Copilot Action Guidelines

#### When User Requests Feature Development:
1. ✅ Check current branch (`git branch --show-current`)
2. ✅ Ensure on correct app branch (`feature/[app-name]-app`)
3. ✅ Create feature branch (`feature/[app-name]-[feature-name]`)
4. ✅ Implement feature with proper testing
5. ✅ Commit with descriptive message
6. ✅ Push feature branch
7. ✅ Merge to app branch (NOT main)

#### When User Requests Bug Fixes:
1. ✅ Create fix branch (`fix/[app-name]-[bug-description]`)
2. ✅ Fix issue with proper testing
3. ✅ Commit with clear description
4. ✅ Merge back to app branch

#### When User Requests App Completion:
1. ✅ Verify all features are working
2. ✅ Run comprehensive tests
3. ✅ Create pull request from app branch to main
4. ✅ Only merge to main after approval

### 🔧 Available Tools for Each App

#### Timesheet App Tools:
- **Workflow Script**: `dev-workflow.ps1` (PowerShell) or `dev-workflow.sh` (Bash)
- **Documentation**: `DEVELOPMENT.md`
- **Commands**:
  - `.\dev-workflow.ps1 start` - Create new feature branch
  - `.\dev-workflow.ps1 test` - Run tests and start server
  - `.\dev-workflow.ps1 commit` - Stage and commit changes
  - `.\dev-workflow.ps1 push` - Push branch to remote
  - `.\dev-workflow.ps1 merge` - Merge to app branch

### 🎯 Integration Strategy

#### Individual Apps → Main FamilyHub:
1. Develop standalone apps in `standalone-apps/`
2. Test independently on different ports (8001, 8002, etc.)
3. When stable, integrate into `FamilyHub/apps/`
4. Update main dashboard and navigation
5. Test integrated functionality

### 🚨 Error Prevention

#### Common Mistakes to Avoid:
- ❌ Never create branches from main for app features
- ❌ Never merge app features directly to main
- ❌ Never run Django commands from wrong directory
- ❌ Never commit without testing
- ❌ Never push broken code
- ❌ Never work on main branch directly

#### Before Every Action:
1. Check current directory: `pwd`
2. Check current branch: `git branch --show-current`
3. Check git status: `git status`
4. Verify server works: Test on appropriate port

### 📊 Project Status Tracking

#### Current Active Branches:
- `main` - Production ready code
- `feature/timesheet-app` - Timesheet application development
- `feature/timesheet-template-fixes` - Template syntax fixes (example)

#### App Development Status:
- **Timesheet**: 🟡 In active development (feature/timesheet-app)
- **Daycare Invoice**: 🟢 Complete, needs integration
- **Employment History**: 🔴 Planning phase
- **Upcoming Payments**: 🔴 Planning phase

### 💡 Best Practices Summary

1. **Branch from app branches, not main**
2. **Test everything before committing**
3. **Use descriptive commit messages**
4. **Merge features to app branch first**
5. **Only merge app to main when complete**
6. **Clean up feature branches after merge**
7. **Always work in correct directory**
8. **Use provided workflow tools**

---

**Remember**: This branching strategy ensures stable development, proper integration testing, and clean production deployments. Always follow this workflow for consistent, professional development! 🎉
