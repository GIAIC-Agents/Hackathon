"""
Interactive script to add QDRANT_URL to .env file.
"""

import os
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent
env_path = project_root / '.env'

print("=" * 60)
print("Qdrant URL Setup")
print("=" * 60)

if not env_path.exists():
    print(f"ERROR: .env file not found at {env_path}")
    print("Please create a .env file first.")
    exit(1)

# Read existing .env
with open(env_path, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.splitlines()

# Check if QDRANT_URL already exists
has_qdrant_url = False
for i, line in enumerate(lines):
    if line.strip().startswith('QDRANT_URL') and not line.strip().startswith('#'):
        has_qdrant_url = True
        print(f"\nQDRANT_URL already exists at line {i+1}:")
        print(f"  {line}")
        break

if not has_qdrant_url:
    print("\nQDRANT_URL is missing from .env file.")
    print("\nPlease add this line to your .env file:")
    print("QDRANT_URL=https://your-cluster-id.cloud.qdrant.io")
    print("\nTo find your Qdrant URL:")
    print("  1. Go to https://cloud.qdrant.io")
    print("  2. Open your cluster")
    print("  3. Go to 'Connection details' or 'API' section")
    print("  4. Copy the URL (format: https://xxxxx-xxxxx-xxxxx.cloud.qdrant.io)")
    print("\nAfter adding QDRANT_URL, run:")
    print("  python scripts/test_chatbot.py")

