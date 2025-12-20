from src.core.config import settings
import os

print(f"Current working directory: {os.getcwd()}")
print(f"QDRANT_URL: {settings.QDRANT_URL}")
print(f"QDRANT_COLLECTION_NAME: {settings.QDRANT_COLLECTION_NAME}")
# Mask keys
gemini_key = settings.GEMINI_API_KEY
print(f"GEMINI_API_KEY set: {bool(gemini_key)} (Length: {len(gemini_key) if gemini_key else 0})")
qdrant_key = settings.QDRANT_API_KEY
print(f"QDRANT_API_KEY set: {bool(qdrant_key)} (Length: {len(qdrant_key) if qdrant_key else 0})")
