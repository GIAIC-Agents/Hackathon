"""
Quick script to check environment variables from .env file.
This helps diagnose what variables are set and what's missing.
"""

import os
from dotenv import load_dotenv

# Load .env from project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

print("Checking environment variables from .env file...")
print("=" * 60)

required_vars = [
    "GEMINI_API_KEY",
    "QDRANT_URL",  # Also checks QDRANT_ENDPOINT
    "QDRANT_API_KEY",
    "QDRANT_COLLECTION"
]

optional_vars = [
    "GEMINI_MODEL",
    "GEMINI_EMBED_MODEL",
    "QDRANT_TOP_K",
    "QDRANT_SCORE_THRESHOLD"
]

print("\nRequired variables:")
for var in required_vars:
    # Special handling for QDRANT_URL - also check QDRANT_ENDPOINT
    if var == "QDRANT_URL":
        value = os.getenv("QDRANT_URL") or os.getenv("QDRANT_ENDPOINT")
        if not value:
            print(f"  [MISSING] {var} (or QDRANT_ENDPOINT): NOT SET")
        else:
            # Show which one is being used
            if os.getenv("QDRANT_URL"):
                print(f"  [OK] QDRANT_URL: {value}")
            else:
                print(f"  [OK] QDRANT_ENDPOINT: {value} (used as QDRANT_URL)")
    else:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "KEY" in var or "API" in var:
                masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
                print(f"  [OK] {var}: {masked}")
            else:
                print(f"  [OK] {var}: {value}")
        else:
            print(f"  [MISSING] {var}: NOT SET")

print("\nOptional variables:")
for var in optional_vars:
    value = os.getenv(var)
    if value:
        print(f"  [OK] {var}: {value}")
    else:
        print(f"  [-] {var}: Using default")

print("\n" + "=" * 60)
print("\nNote: Both QDRANT_URL and QDRANT_ENDPOINT are supported.")
print("If QDRANT_URL/QDRANT_ENDPOINT is missing, add it to your .env file:")
print("  QDRANT_ENDPOINT=https://your-cluster-id.cloud.qdrant.io")
print("\nOr use:")
print("  QDRANT_URL=https://your-cluster-id.cloud.qdrant.io")

