# Local OCR Server - Quick Test Script
# Run this to verify everything is working

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Local OCR Server - Connection Test" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Test if server is running
Write-Host "[1/2] Testing server connection..." -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/health" -Method Get -TimeoutSec 5
    Write-Host "✓ Server is running!" -ForegroundColor Green
    Write-Host "  Model: $($response.model)" -ForegroundColor Gray
    Write-Host "  Status: $($response.status)`n" -ForegroundColor Gray
} catch {
    Write-Host "✗ Server is not responding" -ForegroundColor Red
    Write-Host "  Make sure you ran: python server.py`n" -ForegroundColor Gray
    exit 1
}

# List available models
Write-Host "[2/2] Checking Ollama models..." -ForegroundColor Yellow

try {
    $models = Invoke-RestMethod -Uri "http://localhost:5000/models" -Method Get
    Write-Host "✓ Available models:" -ForegroundColor Green
    foreach ($model in $models.models) {
        Write-Host "  - $model" -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ Could not fetch models" -ForegroundColor Red
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  All tests passed! Server is ready." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Run: ngrok http 5000" -ForegroundColor White
Write-Host "2. Copy the ngrok URL (https://...)" -ForegroundColor White
Write-Host "3. Paste it in Apps Script Settings" -ForegroundColor White
Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
