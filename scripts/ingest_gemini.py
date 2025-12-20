import os
import glob
import logging
import asyncio
from typing import List, Dict
import sys

# Add the parent directory to sys.path to allow imports from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from qdrant_client import QdrantClient
from qdrant_client.http import models
from src.core.config import settings
from src.services.gemini_service import GeminiService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting Gemini ingestion process...")
    
    # Initialize services
    gemini_service = GeminiService()
    qdrant_client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        prefer_grpc=False
    )
    
    collection_name = settings.QDRANT_COLLECTION_NAME
    embedding_size = 768  # Gemini embedding-001 dimension
    
    # 1. Recreate Collection
    logger.info(f"Recreating collection '{collection_name}' with dimension {embedding_size}...")
    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=embedding_size, distance=models.Distance.COSINE)
    )
    logger.info("Collection recreated successfully.")
    
    # 2. Read and Chunk Documents
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'book', 'docs')
    logger.info(f"Scanning for markdown files in {docs_dir}...")
    
    files = glob.glob(f"{docs_dir}/**/*.md", recursive=True)
    logger.info(f"Found {len(files)} markdown files.")
    
    points = []
    point_id = 0
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple chunking by double newline (paragraphs)
            # You might want to use a more sophisticated chunker (e.g., langchain)
            chunks = [c.strip() for c in content.split('\n\n') if c.strip()]
            
            relative_path = os.path.relpath(file_path, docs_dir)
            logger.info(f"Processing {relative_path}: {len(chunks)} chunks")
            
            for chunk in chunks:
                if len(chunk) < 50:  # Skip very short chunks
                    continue
                
                # Generate embedding
                embedding = await gemini_service.get_embedding(chunk)
                
                # Create point
                point = models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "content": chunk,
                        "source": relative_path,
                        "metadata": {"type": "text"}
                    }
                )
                points.append(point)
                point_id += 1
                
                # Batch upsert every 50 points
                if len(points) >= 50:
                    qdrant_client.upsert(
                        collection_name=collection_name,
                        points=points
                    )
                    logger.info(f"Upserted batch of {len(points)} points")
                    points = []
                    
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            
    # Upsert remaining points
    if points:
        qdrant_client.upsert(
            collection_name=collection_name,
            points=points
        )
        logger.info(f"Upserted final batch of {len(points)} points")

    logger.info("Ingestion complete!")

if __name__ == "__main__":
    asyncio.run(main())
