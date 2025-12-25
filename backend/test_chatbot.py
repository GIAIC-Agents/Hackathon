"""
Test script for the chatbot that sends predefined queries and validates responses.
This script tests the connection to Qdrant Cloud and the chatbot functionality.

Usage:
    python scripts/test_chatbot.py
"""

from __future__ import annotations

import os
import sys
from typing import List

# Add parent directory to path to import chatbot
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

# Import from chatbot module
try:
    # Prefer local module import (works when running from backend directory)
    from chatbot import (
        build_config,
        make_clients,
        embed_query,
        search_qdrant,
        build_context,
        ask_groq,
        check_data,
        _payload_text,
        Config,
    )
    from qdrant_client import QdrantClient
except ImportError:
    # Fallback for alternative layouts
    from backend.chatbot import (
        build_config,
        make_clients,
        embed_query,
        search_qdrant,
        build_context,
        ask_groq,
        check_data,
        _payload_text,
        Config,
    )
    from qdrant_client import QdrantClient


def test_qdrant_connection(client: QdrantClient, config: Config) -> bool:
    """Test if Qdrant connection is working."""
    try:
        info = client.get_collection(config.collection)
        print("[OK] Connected to Qdrant Cloud")
        print(f"  Collection: {config.collection}")
        print(f"  Vectors count: {info.points_count}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to connect to Qdrant: {e}")
        return False


def test_embedding(config: Config) -> bool:
    """Test if embedding generation is working."""
    try:
        test_query = "What is robotics?"
        vector = embed_query(test_query, config.embedding_model)
        print("[OK] Embedding generated successfully")
        print(f"  Query: '{test_query}'")
        print(f"  Vector dimension: {len(vector)}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to generate embedding: {e}")
        return False


def test_vector_search(client: QdrantClient, config: Config, query: str) -> List:
    """Test vector search in Qdrant."""
    try:
        query_vector = embed_query(query, config.embedding_model)
        points = search_qdrant(client, config, query_vector)
        print("[OK] Vector search completed")
        print(f"  Query: '{query}'")
        print(f"  Results found: {len(points)}")
        if points:
            print(f"  Top score: {points[0].score:.4f}")
        return points
    except Exception as e:
        print(f"[ERROR] Vector search failed: {e}")
        return []


def test_chatbot_query(
    client: QdrantClient,
    groq_client,
    config: Config,
    query: str,
) -> str | None:
    """Test a complete chatbot query end-to-end."""
    try:
        print("\n" + "=" * 60)
        print("Query: " + query)
        print("=" * 60)

        # Step 1: Generate embedding
        query_vector = embed_query(query, config.embedding_model)

        # Step 2: Search Qdrant
        points = search_qdrant(client, config, query_vector)

        if not points:
            print("[WARNING] No relevant context found in Qdrant.")
            return None

        # Step 3: Build context
        context = build_context(points)
        print("\nRetrieved Context (" + str(len(points)) + " results):")
        print("-" * 60)
        for i, point in enumerate(points[:3], 1):  # Show top 3
            payload_text = _payload_text(point.payload or {})
            print(str(i) + ". [Score: " + str(point.score) + "] " + payload_text[:150] + "...")
        print("-" * 60)

        # Step 4: Generate answer
        answer = ask_groq(query, context, groq_client, config.groq_model)
        print("\nAnswer:\n" + answer)
        print("=" * 60 + "\n")

        return answer
    except Exception as e:
        print("[ERROR] Query failed: " + str(e))
        import traceback
        traceback.print_exc()
        return None


def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("Testing Qdrant Cloud + Groq Chatbot")
    print("=" * 60)

    # Load configuration
    try:
        config = build_config()
        print("\n[OK] Configuration loaded successfully")
    except Exception as e:
        print("\n[ERROR] Failed to load configuration: " + str(e))
        print("\nPlease make sure your .env file contains:")
        print("  - GEMINI_API_KEY")
        print("  - GROQ_API_KEY")
        print("  - QDRANT_URL")
        print("  - QDRANT_API_KEY")
        print("  - QDRANT_COLLECTION")
        print("\nMake sure .env file is in the project root directory.")
        sys.exit(1)

    # Initialize clients
    try:
        qdrant_client, groq_client = make_clients(config)
        print("[OK] Clients initialized successfully\n")
    except Exception as e:
        print("[ERROR] Failed to initialize clients: " + str(e))
        sys.exit(1)

    # Test 1: Qdrant connection
    print("\n[Test 1] Testing Qdrant Connection...")
    if not test_qdrant_connection(qdrant_client, config):
        sys.exit(1)

    # Test 2: Check data
    print("\n[Test 2] Checking Qdrant Data...")
    check_data(qdrant_client, config)

    # Test 3: Embedding generation
    print("\n[Test 3] Testing Embedding Generation...")
    if not test_embedding(config):
        sys.exit(1)

    # Test 4: Vector search
    print("\n[Test 4] Testing Vector Search...")
    test_query = "What is artificial intelligence in robotics?"
    points = test_vector_search(qdrant_client, config, test_query)
    if not points:
        print("[WARNING] No results found for test query. Make sure your collection has data.")

    # Test 5: Full chatbot queries
    print("\n[Test 5] Testing Full Chatbot Queries...")
    test_queries = [
        "What is robotics?",
        "Explain humanoid robots",
        "What are the applications of AI in robotics?",
        "Tell me about robot kinematics",
        "How do sensors work in robots?",
    ]

    successful_queries = 0
    for query in test_queries:
        answer = test_chatbot_query(qdrant_client, groq_client, config, query)
        if answer:
            successful_queries += 1

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print("Total queries tested: " + str(len(test_queries)))
    print("Successful queries: " + str(successful_queries))
    print("Failed queries: " + str(len(test_queries) - successful_queries))

    if successful_queries > 0:
        print("\n[SUCCESS] Chatbot is working! You can now run:")
        print("  python scripts/chatbot.py")
    else:
        print("\n[WARNING] Some queries failed. Check your Qdrant collection has data.")


if __name__ == "__main__":
    run_tests()

