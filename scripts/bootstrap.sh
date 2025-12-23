#!/usr/bin/env bash
# Bootstrap helper for Unix-like shells (Git Bash / WSL / macOS / Linux)
# Usage: ./scripts/bootstrap.sh [--dev]
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if [ ! -d ".venv" ]; then
  echo "Creating virtualenv: .venv"
  python3 -m venv .venv
else
  echo ".venv already exists"
fi

VENV_PY="$REPO_ROOT/.venv/bin/python"
echo "Upgrading pip in venv..."
"$VENV_PY" -m pip install --upgrade pip

echo "Installing runtime requirements into venv..."
"$VENV_PY" -m pip install -r requirements.txt

if [ "${1-}" = "--dev" ]; then
  echo "Installing dev requirements into venv..."
  "$VENV_PY" -m pip install -r requirements-dev.txt
fi

echo "\nBootstrap finished. Activate the venv with:"
echo "source .venv/bin/activate"
return 0
