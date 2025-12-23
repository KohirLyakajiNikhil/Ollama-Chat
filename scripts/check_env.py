#!/usr/bin/env python
"""Simple preflight check to verify key dependencies are available in the
current Python environment (useful to detect if packages are missing from
an activated venv)."""
import importlib
import json
import sys

REQUIRED = [
    ("dotenv", "python-dotenv"),
    ("ollama", "ollama"),
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
]

missing = []

for module, pkg in REQUIRED:
    try:
        importlib.import_module(module)
    except Exception:
        missing.append(pkg)

res = {"ok": len(missing) == 0, "missing": missing}
print(json.dumps(res, indent=2))

if not res["ok"]:
    print("\nTip: activate the virtualenv and run:", file=sys.stderr)
    print("  python -m pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)

print("All required packages appear to be installed.")
sys.exit(0)
