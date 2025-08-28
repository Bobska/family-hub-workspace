#!/bin/bash

# FamilyHub Timesheet Development Workflow Script
# Usage: ./dev-workflow.sh [command]

PROJECT_DIR="C:/Users/Dmitry/OneDrive/Development/myprojects/family-hub-workspace/standalone-apps/timesheet"
MAIN_BRANCH="main"
APP_BRANCH="feature/timesheet-app"

case "$1" in
    "start")
        echo "🚀 Starting development workflow..."
        cd "$PROJECT_DIR"
        
        # Ensure we're on main and up to date
        git checkout main
        git pull origin main
        
        # Create feature branch
        read -p "Enter feature branch name (e.g., feature/new-feature): " BRANCH_NAME
        git checkout -b "$BRANCH_NAME"
        
        echo "✅ Created and switched to branch: $BRANCH_NAME"
        echo "💡 Remember to commit regularly and push your branch when ready for review!"
        ;;
        
    "test")
        echo "🧪 Running tests and starting development server..."
        cd "$PROJECT_DIR"
        
        # Run Django checks
        python manage.py check
        
        # Check for migration issues
        python manage.py makemigrations --dry-run
        
        # Start development server
        echo "🌐 Starting server on http://127.0.0.1:8001/"
        python manage.py runserver 8001
        ;;
        
    "commit")
        echo "💾 Committing changes..."
        cd "$PROJECT_DIR"
        
        # Show status
        git status
        
        # Add all changes
        git add .
        
        # Get commit message
        read -p "Enter commit message: " COMMIT_MSG
        git commit -m "$COMMIT_MSG"
        
        echo "✅ Changes committed!"
        echo "💡 Use './dev-workflow.sh push' to push to remote"
        ;;
        
    "push")
        echo "📤 Pushing branch to remote..."
        cd "$PROJECT_DIR"
        
        CURRENT_BRANCH=$(git branch --show-current)
        git push origin "$CURRENT_BRANCH"
        
        echo "✅ Branch pushed to remote!"
        echo "💡 Create a pull request at: https://github.com/Bobska/family-hub-workspace/pulls"
        ;;
        
    "merge")
        echo "🔀 Merging to main branch..."
        cd "$PROJECT_DIR"
        
        CURRENT_BRANCH=$(git branch --show-current)
        
        # Switch to main and update
        git checkout main
        git pull origin main
        
        # Merge feature branch
        git merge "$CURRENT_BRANCH"
        git push origin main
        
        # Clean up feature branch
        read -p "Delete feature branch '$CURRENT_BRANCH'? (y/N): " DELETE_BRANCH
        if [[ $DELETE_BRANCH =~ ^[Yy]$ ]]; then
            git branch -d "$CURRENT_BRANCH"
            git push origin --delete "$CURRENT_BRANCH"
            echo "✅ Feature branch deleted"
        fi
        
        echo "✅ Changes merged to main!"
        ;;
        
    "status")
        echo "📊 Project Status..."
        cd "$PROJECT_DIR"
        
        echo "Current branch: $(git branch --show-current)"
        echo "Git status:"
        git status --short
        echo ""
        echo "Recent commits:"
        git log --oneline -5
        ;;
        
    *)
        echo "🔧 FamilyHub Timesheet Development Workflow"
        echo ""
        echo "Available commands:"
        echo "  start   - Create new feature branch from main"
        echo "  test    - Run tests and start development server"
        echo "  commit  - Stage and commit changes"
        echo "  push    - Push current branch to remote"
        echo "  merge   - Merge current branch to main"
        echo "  status  - Show project and git status"
        echo ""
        echo "Example usage:"
        echo "  ./dev-workflow.sh start"
        echo "  ./dev-workflow.sh test"
        echo "  ./dev-workflow.sh commit"
        echo "  ./dev-workflow.sh push"
        ;;
esac
