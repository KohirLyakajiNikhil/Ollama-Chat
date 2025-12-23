<#
PowerShell bootstrap helper for Windows

Usage (PowerShell):
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned  # optional if scripts are blocked
  .\scripts\bootstrap.ps1 [-Dev]

This script creates a .venv folder (if missing), installs requirements into that venv's Python,
and prints activation instructions for PowerShell / CMD.
#>
param(
    [switch]$Dev
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Push-Location $repo

if (-not (Test-Path -Path .venv)) {
    Write-Host "Creating virtual environment: .venv"
    python -m venv .venv
} else {
    Write-Host ".venv already exists"
}

$venvPython = Join-Path -Path $repo -ChildPath ".venv\Scripts\python.exe"
Write-Host "Upgrading pip in venv"
& $venvPython -m pip install --upgrade pip

Write-Host "Installing runtime requirements into venv"
& $venvPython -m pip install -r requirements.txt

if ($Dev) {
    Write-Host "Installing developer requirements into venv"
    & $venvPython -m pip install -r requirements-dev.txt
}

Write-Host "\nBootstrap finished. Activate the virtualenv in your current PowerShell session with:"
Write-Host ". .venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "(Or in CMD: .venv\Scripts\activate)" -ForegroundColor Cyan
Pop-Location

return 0
