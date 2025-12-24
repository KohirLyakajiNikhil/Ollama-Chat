import os
import sys

# Ensure the local package in src/ is importable during tests
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
SYS_SRC = os.path.join(REPO_ROOT, "src")
if SYS_SRC not in sys.path:
    sys.path.insert(0, SYS_SRC)
