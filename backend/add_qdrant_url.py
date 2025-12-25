"""
Helper script to add QDRANT_URL to .env file if missing.
"""

import os
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent
env_path = project_root / '.env'

print(f"Checking .env file at: {env_path}")

if not env_path.exists():
    print("ERROR: .env file not found!")
    print(f"Please create .env file at: {env_path}")
    exit(1)

# Read existing .env
with open(env_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check if QDRANT_URL exists
has_qdrant_url = any('QDRANT_URL' in line and not line.strip().startswith('#') for line in lines)

if has_qdrant_url:
    print("QDRANT_URL already exists in .env file")
else:
    print("QDRANT_URL is missing. Please add it manually to your .env file:")
    print("\nAdd this line:")
    print("QDRANT_URL=https://your-cluster-id.cloud.qdrant.io")
    print("\nReplace 'your-cluster-id' with your actual Qdrant Cloud cluster ID.")
    print("\nYou can find your Qdrant URL in:")
    print("  - Qdrant Cloud Dashboard -> Your Cluster -> Connection details")
    print("\nExample format: https://xxxxx-xxxxx-xxxxx.cloud.qdrant.io")

