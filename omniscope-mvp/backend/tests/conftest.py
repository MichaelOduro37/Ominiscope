import os
import sys

# Ensure the backend package root is on sys.path so `from app import ...` works during tests
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
