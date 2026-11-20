param(
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$venv = Join-Path $PSScriptRoot ".venv-desktop"
$python = Join-Path $venv "Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "Creating desktop build environment with Python 3.12..."
    py -3.12 -m venv $venv

    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $python)) {
        throw "Python 3.12 is required. Install Python 3.12 x64, then run this script again."
    }
}

if (-not $SkipInstall) {
    & $python -m pip install --upgrade pip
    & $python -m pip install -r requirements-desktop.txt
}

foreach ($folder in @("build", "dist", "release")) {
    if (Test-Path $folder) {
        Remove-Item -Recurse -Force $folder
    }
}

Write-Host "Building Deathdream as a one-folder Windows application..."
& $python -m PyInstaller --clean --noconfirm Deathdream.spec

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller build failed."
}

New-Item -ItemType Directory -Path "release" | Out-Null

$zipPath = Join-Path $PSScriptRoot "release\Deathdream-Windows.zip"
Compress-Archive -Path ".\dist\Deathdream\*" -DestinationPath $zipPath -CompressionLevel Optimal -Force

$hash = Get-FileHash -Algorithm SHA256 $zipPath
$hashLine = "$($hash.Hash.ToLower())  Deathdream-Windows.zip"
Set-Content -Path ".\release\SHA256SUMS.txt" -Value $hashLine -Encoding ascii

Write-Host ""
Write-Host "Build complete:"
Write-Host "  release\Deathdream-Windows.zip"
Write-Host "  release\SHA256SUMS.txt"
Write-Host ""
Write-Host "Upload the ZIP to itch.io as the downloadable Windows version."
