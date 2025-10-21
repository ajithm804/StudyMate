# Master script to start all StudyMate services

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 78) -ForegroundColor Cyan
Write-Host "  🚀 STARTING STUDYMATE SERVICES" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 78) -ForegroundColor Cyan

$projectRoot = Split-Path -Parent $PSScriptRoot

# Check if virtual environment exists
if (-not (Test-Path "$projectRoot\.venv")) {
    Write-Host "`n⚠️  Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv "$projectRoot\.venv"
    Write-Host "✅ Virtual environment created`n" -ForegroundColor Green
}

# Function to start a service in a new terminal
function Start-Service {
    param(
        [string]$Name,
        [string]$Path,
        [string]$Command
    )
    
    Write-Host "🔄 Starting $Name..." -ForegroundColor Cyan
    
    $fullPath = Join-Path $projectRoot $Path
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$fullPath'; $Command"
    
    Write-Host "✅ $Name terminal opened" -ForegroundColor Green
}

# Start AI Service
Write-Host "`n📦 AI Service (Python - Port 5000)" -ForegroundColor Yellow
Start-Service -Name "AI Service" -Path "ai_service" -Command "& '$projectRoot\.venv\Scripts\Activate.ps1'; python app.py"

Start-Sleep -Seconds 2

# Start Backend
Write-Host "`n📦 Backend API (Node.js - Port 3000)" -ForegroundColor Yellow
Start-Service -Name "Backend" -Path "backend" -Command "npm start"

Start-Sleep -Seconds 2

# Start Frontend
Write-Host "`n📦 Frontend (React - Port 5173)" -ForegroundColor Yellow
Start-Service -Name "Frontend" -Path "frontend" -Command "npm run dev"

Write-Host "`n" + ("=" * 80) -ForegroundColor Cyan
Write-Host "✅ ALL SERVICES STARTED!" -ForegroundColor Green
Write-Host ("=" * 80) -ForegroundColor Cyan

Write-Host "`n📍 Service URLs:" -ForegroundColor Yellow
Write-Host "   🌐 Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "   🔧 Backend:   http://localhost:3000" -ForegroundColor White
Write-Host "   🤖 AI Service: http://localhost:5000" -ForegroundColor White

Write-Host "`n💡 Tip: Press Ctrl+C in each terminal to stop services`n" -ForegroundColor Cyan
