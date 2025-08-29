# FamilyHub Development Tools Setup
# Ensures GNU Make is properly installed and accessible

$ErrorActionPreference = "Stop"

Write-Host "🔧 FamilyHub Development Tools Setup" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check if make is already available
if (Get-Command make -ErrorAction SilentlyContinue) {
    Write-Host "✅ GNU Make is already available" -ForegroundColor Green
    make --version
    exit 0
}

Write-Host "Installing GNU Make..." -ForegroundColor Yellow

# Install GNU Make via winget if not already installed
try {
    winget install --id ezwinports.make --silent --accept-source-agreements
    Write-Host "✅ GNU Make installed via winget" -ForegroundColor Green
}
catch {
    Write-Host "⚠️ WinGet installation failed, checking existing installation..." -ForegroundColor Yellow
}

# Create tools directory
$toolsDir = "$env:USERPROFILE\Tools\bin"
Write-Host "Creating tools directory: $toolsDir" -ForegroundColor Yellow
New-Item -ItemType Directory -Path $toolsDir -Force | Out-Null

# Find and copy make.exe
$makeLocations = @(
    "$env:USERPROFILE\AppData\Local\Microsoft\WinGet\Packages\ezwinports.make_Microsoft.Winget.Source_8wekyb3d8bbwe\bin\make.exe",
    "C:\Program Files\Make\bin\make.exe",
    "C:\Tools\make\bin\make.exe"
)

$makeFound = $false
foreach ($location in $makeLocations) {
    if (Test-Path $location) {
        Write-Host "Found make.exe at: $location" -ForegroundColor Green
        Copy-Item $location $toolsDir -Force
        $makeFound = $true
        break
    }
}

if (-not $makeFound) {
    Write-Host "❌ Could not find make.exe. Please install GNU Make manually." -ForegroundColor Red
    Write-Host "   Try: winget install ezwinports.make" -ForegroundColor Yellow
    exit 1
}

# Add to PATH permanently
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$toolsDir*") {
    $newPath = "$currentPath;$toolsDir"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "✅ Added $toolsDir to user PATH" -ForegroundColor Green
} else {
    Write-Host "✅ Path already contains $toolsDir" -ForegroundColor Green
}

# Update current session PATH
$env:PATH += ";$toolsDir"

# Test installation
Write-Host ""
Write-Host "Testing GNU Make installation..." -ForegroundColor Yellow
if (Get-Command make -ErrorAction SilentlyContinue) {
    Write-Host "✅ GNU Make installation successful!" -ForegroundColor Green
    make --version
    Write-Host ""
    Write-Host "🎉 Development tools setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor Cyan
    Write-Host "  make help          # Show all available commands"
    Write-Host "  make dev           # Start development environment"
    Write-Host "  make quick         # Start PostgreSQL only"
    Write-Host "  make status        # Check service status"
} else {
    Write-Host "❌ GNU Make installation failed" -ForegroundColor Red
    Write-Host "Please restart your terminal and try again" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📝 Note: You may need to restart your terminal for PATH changes to take effect." -ForegroundColor Yellow
