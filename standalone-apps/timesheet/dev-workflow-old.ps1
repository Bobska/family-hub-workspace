# FamilyHub Timesheet Development Workflow Script (PowerShell)
# Usage: .\dev-workflow.ps1 [command]

param(
    [Parameter(Position=0)]
    [string]$Command
)

$ProjectDir = "C:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace\standalone-apps\timesheet"
$MainBranch = "main"
$AppBranch = "feature/timesheet-app"

function Start-Development {
    Write-Host "🚀 Starting development workflow..." -ForegroundColor Green
    Set-Location $ProjectDir
    
    # Ensure we're on app branch and up to date
    git checkout $AppBranch
    git pull origin $AppBranch
    
    # Create feature branch from app branch
    $BranchName = Read-Host "Enter feature branch name (e.g., feature/timesheet-validation, fix/template-bug)"
    git checkout -b $BranchName
    
    Write-Host "✅ Created and switched to branch: $BranchName" -ForegroundColor Green
    Write-Host "💡 This branch is based on: $AppBranch" -ForegroundColor Yellow
    Write-Host "💡 When ready, merge back to $AppBranch, then $AppBranch → $MainBranch" -ForegroundColor Yellow
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
    Write-Host "🔀 Merging branch..." -ForegroundColor Green
    Set-Location $ProjectDir
    
    $CurrentBranch = git branch --show-current
    
    # Determine merge target
    if ($CurrentBranch -eq $AppBranch) {
        # Merging app branch to main
        Write-Host "🎯 Merging $AppBranch to $MainBranch" -ForegroundColor Cyan
        git checkout $MainBranch
        git pull origin $MainBranch
        git merge $AppBranch
        git push origin $MainBranch
        Write-Host "✅ App merged to main! 🎉" -ForegroundColor Green
    } else {
        # Merging feature/fix branch to app branch
        Write-Host "🎯 Merging $CurrentBranch to $AppBranch" -ForegroundColor Cyan
        git checkout $AppBranch
        git pull origin $AppBranch
        git merge $CurrentBranch
        git push origin $AppBranch
        
        # Clean up feature branch
        $DeleteBranch = Read-Host "Delete feature branch '$CurrentBranch'? (y/N)"
        if ($DeleteBranch -match "^[Yy]$") {
            git branch -d $CurrentBranch
            git push origin --delete $CurrentBranch
            Write-Host "✅ Feature branch deleted" -ForegroundColor Green
        }
        Write-Host "✅ Feature merged to app branch!" -ForegroundColor Green
    }
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
    Write-Host "🌿 Branching Strategy:" -ForegroundColor Yellow
    Write-Host "  main <- feature/timesheet-app <- feature/your-feature"
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host "  start   - Create new feature branch from app branch"
    Write-Host "  test    - Run tests and start development server"
    Write-Host "  commit  - Stage and commit changes"
    Write-Host "  push    - Push current branch to remote"
    Write-Host "  merge   - Merge current branch (feature->app or app->main)"
    Write-Host "  status  - Show project and git status"
    Write-Host ""
    Write-Host "Example workflow:" -ForegroundColor Yellow
    Write-Host "  .\dev-workflow.ps1 start     # Create feature branch"
    Write-Host "  # ... make changes ..."
    Write-Host "  .\dev-workflow.ps1 commit    # Commit changes"
    Write-Host "  .\dev-workflow.ps1 push      # Push feature branch"
    Write-Host "  .\dev-workflow.ps1 merge     # Merge to app branch"
    Write-Host ""
    Write-Host "  # When app is complete:"
    Write-Host "  git checkout feature/timesheet-app"
    Write-Host "  .\dev-workflow.ps1 merge     # Merge app to main"
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
