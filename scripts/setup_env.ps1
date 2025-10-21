# Setup script for first-time installation

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 78) -ForegroundColor Cyan
Write-Host "  🔧 STUDYMATE ENVIRONMENT SETUP" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 78) -ForegroundColor Cyan

$projectRoot = Split-Path -Parent $PSScriptRoot

# Step 1: Create Virtual Environment
Write-Host "`n[1/4] Creating Python virtual environment..." -ForegroundColor Yellow

if (Test-Path "$projectRoot\.venv") {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv "$projectRoot\.venv"
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Step 2: Install Python dependencies
Write-Host "`n[2/4] Installing Python dependencies..." -ForegroundColor Yellow
& "$projectRoot\.venv\Scripts\Activate.ps1"
pip install -r "$projectRoot\ai_service\requirements.txt"
Write-Host "✅ Python dependencies installed" -ForegroundColor Green

# Step 3: Install Backend dependencies
Write-Host "`n[3/4] Installing Backend (Node.js) dependencies..." -ForegroundColor Yellow
Set-Location "$projectRoot\backend"
npm install
Write-Host "✅ Backend dependencies installed" -ForegroundColor Green

# Step 4: Install Frontend dependencies
Write-Host "`n[4/4] Installing Frontend (React) dependencies..." -ForegroundColor Yellow
Set-Location "$projectRoot\frontend"
npm install
Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green

Set-Location $projectRoot

Write-Host "`n" + ("=" * 80) -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host ("=" * 80) -ForegroundColor Cyan

Write-Host "`n📝 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Place NCERT PDFs in: ai_service\data\raw_pdfs\" -ForegroundColor White
Write-Host "   2. Run: python scripts\ingest_pdfs.py" -ForegroundColor White
Write-Host "   3. Run: python scripts\rebuild_embeddings.py" -ForegroundColor White
Write-Host "   4. Run: .\scripts\start_all.ps1" -ForegroundColor White
Write-Host ""
