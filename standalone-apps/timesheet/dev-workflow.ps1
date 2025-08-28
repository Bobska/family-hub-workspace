# FamilyHub Timesheet Development Workflow Script (PowerShell)
# Usage: .\dev-workflow.ps1 [command]

param(
    [Parameter(Position=0)]
    [string]$Command
)

$ProjectDir = "C:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace\standalone-apps\timesheet"
$MainBranch = "main"

function Start-Development {
    Write-Host "🚀 Starting development workflow..." -ForegroundColor Green
    Set-Location $ProjectDir
    
    # Ensure we're on main and up to date
    git checkout main
    git pull origin main
    
    # Create feature branch
    $BranchName = Read-Host "Enter feature branch name (e.g., feature/new-feature)"
    git checkout -b $BranchName
    
    Write-Host "✅ Created and switched to branch: $BranchName" -ForegroundColor Green
    Write-Host "💡 Remember to commit regularly and push your branch when ready for review!" -ForegroundColor Yellow
}

function Test-Application {
    Write-Host "🧪 Running tests and starting development server..." -ForegroundColor Green
    Set-Location $ProjectDir
    
    # Run Django checks
    python manage.py check
    
    # Check for migration issues
    python manage.py makemigrations --dry-run
    
    # Start development server
    Write-Host "🌐 Starting server on http://127.0.0.1:8001/" -ForegroundColor Cyan
    python manage.py runserver 8001
}

function Commit-Changes {
    Write-Host "💾 Committing changes..." -ForegroundColor Green
    Set-Location $ProjectDir
    
    # Show status
    git status
    
    # Add all changes
    git add .
    
    # Get commit message
    $CommitMsg = Read-Host "Enter commit message"
    git commit -m $CommitMsg
    
    Write-Host "✅ Changes committed!" -ForegroundColor Green
    Write-Host "💡 Use '.\dev-workflow.ps1 push' to push to remote" -ForegroundColor Yellow
}

function Push-Branch {
    Write-Host "📤 Pushing branch to remote..." -ForegroundColor Green
    Set-Location $ProjectDir
    
    $CurrentBranch = git branch --show-current
    git push origin $CurrentBranch
    
    Write-Host "✅ Branch pushed to remote!" -ForegroundColor Green
    Write-Host "💡 Create a pull request at: https://github.com/Bobska/family-hub-workspace/pulls" -ForegroundColor Yellow
}

function Merge-Branch {
    Write-Host "🔀 Merging to main branch..." -ForegroundColor Green
    Set-Location $ProjectDir
    
    $CurrentBranch = git branch --show-current
    
    # Switch to main and update
    git checkout main
    git pull origin main
    
    # Merge feature branch
    git merge $CurrentBranch
    git push origin main
    
    # Clean up feature branch
    $DeleteBranch = Read-Host "Delete feature branch '$CurrentBranch'? (y/N)"
    if ($DeleteBranch -match "^[Yy]$") {
        git branch -d $CurrentBranch
        git push origin --delete $CurrentBranch
        Write-Host "✅ Feature branch deleted" -ForegroundColor Green
    }
    
    Write-Host "✅ Changes merged to main!" -ForegroundColor Green
}

function Show-Status {
    Write-Host "📊 Project Status..." -ForegroundColor Green
    Set-Location $ProjectDir
    
    $CurrentBranch = git branch --show-current
    Write-Host "Current branch: $CurrentBranch" -ForegroundColor Cyan
    Write-Host "Git status:" -ForegroundColor Cyan
    git status --short
    Write-Host ""
    Write-Host "Recent commits:" -ForegroundColor Cyan
    git log --oneline -5
}

function Show-Help {
    Write-Host "🔧 FamilyHub Timesheet Development Workflow" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host "  start   - Create new feature branch from main"
    Write-Host "  test    - Run tests and start development server"
    Write-Host "  commit  - Stage and commit changes"
    Write-Host "  push    - Push current branch to remote"
    Write-Host "  merge   - Merge current branch to main"
    Write-Host "  status  - Show project and git status"
    Write-Host ""
    Write-Host "Example usage:" -ForegroundColor Yellow
    Write-Host "  .\dev-workflow.ps1 start"
    Write-Host "  .\dev-workflow.ps1 test"
    Write-Host "  .\dev-workflow.ps1 commit"
    Write-Host "  .\dev-workflow.ps1 push"
}

# Main script logic
switch ($Command) {
    "start" { Start-Development }
    "test" { Test-Application }
    "commit" { Commit-Changes }
    "push" { Push-Branch }
    "merge" { Merge-Branch }
    "status" { Show-Status }
    default { Show-Help }
}
