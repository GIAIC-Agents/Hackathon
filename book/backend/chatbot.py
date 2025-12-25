"""
Terminal chatbot that answers questions using book vectors stored in Qdrant
and Gemini for reasoning.

Environment variables (use a .env file locally if you like):
- GEMINI_API_KEY        : Gemini API key
- GEMINI_MODEL          : (optional) defaults to "gemini-1.5-flash"
- GEMINI_EMBED_MODEL    : (optional) defaults to "models/text-embedding-004"
- QDRANT_URL or QDRANT_ENDPOINT : Qdrant Cloud endpoint (e.g., https://xxxx.cloud.qdrant.io)
- QDRANT_API_KEY        : Qdrant API key
- QDRANT_COLLECTION     : Name of the collection containing the book vectors
- QDRANT_TOP_K          : (optional) defaults to 5
- QDRANT_SCORE_THRESHOLD: (optional) defaults to 0.15

Usage:
  python scripts/chatbot.py            # starts the chat loop
  python scripts/chatbot.py --check    # fetches a few sample points to verify data
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from typing import Iterable, List

import google.generativeai as genai
try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore[assignment]
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


NO_INFO_MESSAGE = (
    "The knowledge base does not contain enough information to answer "
    "this question."
)

FALLBACK_HEADER = (
    "AI response unavailable. Showing best matched content from the "
    "knowledge base:"
)


def _load_env() -> None:
    if load_dotenv:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(file_dir)

        candidate_paths = [
            os.path.join(file_dir, ".env"),
            os.path.join(os.getcwd(), ".env"),
            os.path.join(parent_dir, ".env"),
        ]

        for env_path in candidate_paths:
            if os.path.exists(env_path):
                load_dotenv(env_path)
                return

        load_dotenv()  # Fallback to default behavior


def _require_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


@dataclass
class Config:
    gemini_api_key: str
    groq_api_key: str
    qdrant_url: str
    qdrant_api_key: str
    collection: str
    top_k: int = 5
    score_threshold: float = 0.15
    model: str = "gemini-1.5-flash"
    embedding_model: str = "models/text-embedding-004"
    groq_model: str = "llama-3.1-70b-versatile"


def build_config() -> Config:
    _load_env()
    # Support both QDRANT_URL and QDRANT_ENDPOINT for compatibility
    qdrant_url = os.getenv("QDRANT_URL") or os.getenv("QDRANT_ENDPOINT")
    if not qdrant_url:
        raise RuntimeError("Missing environment variable: QDRANT_URL or QDRANT_ENDPOINT")
    
    return Config(
        gemini_api_key=_require_env("GEMINI_API_KEY"),
        groq_api_key=_require_env("GROQ_API_KEY"),
        qdrant_url=qdrant_url,
        qdrant_api_key=_require_env("QDRANT_API_KEY"),
        collection=_require_env("QDRANT_COLLECTION"),
        top_k=int(os.getenv("QDRANT_TOP_K", "5")),
        score_threshold=float(os.getenv("QDRANT_SCORE_THRESHOLD", "0.15")),
        model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        embedding_model=os.getenv("GEMINI_EMBED_MODEL", "models/text-embedding-004"),
        groq_model=os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
    )


def make_clients(config: Config) -> tuple[QdrantClient, "OpenAI"]:
    genai.configure(api_key=config.gemini_api_key)
    if OpenAI is None:
        raise RuntimeError(
            "Missing dependency 'openai'. Install it with: pip install openai"
        )
    groq_client = OpenAI(
        api_key=config.groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    )
    qdrant = QdrantClient(
        url=config.qdrant_url,
        api_key=config.qdrant_api_key,
    )
    return qdrant, groq_client


def embed_query(text: str, model: str) -> List[float]:
    response = genai.embed_content(
        model=model,
        content=text,
        task_type="retrieval_query",
    )
    embedding = response.get("embedding")
    if not embedding:
        raise RuntimeError("Gemini embedding response did not contain 'embedding'")
    return embedding


def search_qdrant(
    client: QdrantClient,
    config: Config,
    query_vector: Iterable[float],
) -> List[rest.ScoredPoint]:
    # Use query_points for newer qdrant-client versions (v1.6+)
    results = client.query_points(
        collection_name=config.collection,
        query=list(query_vector),  # Convert to list if needed
        limit=config.top_k,
        score_threshold=config.score_threshold,
        with_payload=True,
    )
    # query_points returns a QueryResponse with points attribute
    return (
        list(results.points)
        if hasattr(results, "points") and results.points
        else []
    )


def _payload_text(payload: dict) -> str:
    """Extract human-readable text from common payload keys."""
    preferred_keys = ("text", "chunk", "content", "page_content", "body")
    for key in preferred_keys:
        if key in payload and isinstance(payload[key], str):
            return payload[key]
    # Fallback to a compact string of all values
    return " ".join(str(v) for v in payload.values())


def build_context(points: List[rest.ScoredPoint]) -> str:
    snippets = []
    for idx, p in enumerate(points, 1):
        payload_text = _payload_text(p.payload or {})
        snippets.append(f"{idx}. {payload_text}")
    return "\n\n".join(snippets)


def ask_gemini(question: str, context: str, model: str) -> str:
    prompt = (
        "You are an expert AI assistant for a Retrieval-Augmented Generation "
        "(RAG) chatbot.\n\n"
        "You will receive:\n"
        "1) A user question\n"
        "2) Retrieved context from a vector database (Qdrant)\n\n"
        "YOUR RULES:\n"
        "- Answer ONLY using the provided context.\n"
        "- Do NOT use outside knowledge.\n"
        "- Do NOT hallucinate or guess.\n"
        "- If the context fully answers the question, give a clear, concise, "
        "well-structured answer.\n"
        "- If the context partially answers the question, answer only the "
        "available part and clearly say what is missing.\n"
        "- If the context does NOT contain the answer, say:\n"
        '  "The knowledge base does not contain enough information '
        'to answer this question."\n\n'
        "FALLBACK BEHAVIOR (IMPORTANT):\n"
        "- If the AI model cannot generate a response due to rate limits, "
        "quota issues, or system errors,\n"
        "  return the most relevant retrieved context as the final answer.\n"
        "- When falling back, format the response as:\n"
        '  "AI response unavailable. Showing best matched content from the '
        'knowledge base:"\n'
        "  followed by the retrieved context text.\n\n"
        "STYLE:\n"
        "- Use simple, clear English\n"
        "- Be factual and technical\n"
        "- Avoid unnecessary verbosity\n"
        "- Do not mention internal system details, APIs, or models\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION:\n{question}\n\n"
        "FINAL ANSWER:\n"
    )
    # Ensure model name has 'models/' prefix for newer API versions
    if not model.startswith("models/"):
        model_name = f"models/{model}"
    else:
        model_name = model

    # Map deprecated model names to available ones
    model_mapping = {
        "models/gemini-1.5-flash": "models/gemini-2.0-flash",
        "models/gemini-1.5-pro": "models/gemini-2.0-flash",
    }
    model_name = model_mapping.get(model_name, model_name)

    chat_model = genai.GenerativeModel(model_name)
    try:
        response = chat_model.generate_content(prompt)
    except Exception:
        return FALLBACK_HEADER + "\n" + context
    if not response.text:
        return FALLBACK_HEADER + "\n" + context
    return response.text.strip()


def ask_groq(question: str, context: str, client: "OpenAI", model: str) -> str:
    system_prompt = (
        "You are an expert AI assistant for a Retrieval-Augmented Generation "
        "(RAG) chatbot.\n\n"
        "You will receive:\n"
        "1) A user question\n"
        "2) Retrieved context from a vector database (Qdrant)\n\n"
        "YOUR RULES:\n"
        "- Answer ONLY using the provided context.\n"
        "- Do NOT use outside knowledge.\n"
        "- Do NOT hallucinate or guess.\n"
        "- If the context fully answers the question, give a clear, concise, "
        "well-structured answer.\n"
        "- If the context partially answers the question, answer only the "
        "available part and clearly say what is missing.\n"
        "- If the context does NOT contain the answer, say:\n"
        '  "The knowledge base does not contain enough information '
        'to answer this question."\n\n'
        "FALLBACK BEHAVIOR (IMPORTANT):\n"
        "- If the AI model cannot generate a response due to rate limits, "
        "quota issues, or system errors,\n"
        "  return the most relevant retrieved context as the final answer.\n"
        "- When falling back, format the response as:\n"
        '  "AI response unavailable. Showing best matched content from the '
        'knowledge base:"\n'
        "  followed by the retrieved context text.\n\n"
        "STYLE:\n"
        "- Use simple, clear English\n"
        "- Be factual and technical\n"
        "- Avoid unnecessary verbosity\n"
        "- Do not mention internal system details, APIs, or models\n"
    )
    user_message = f"CONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nFINAL ANSWER:\n"
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
            top_p=0.9,
        )
    except Exception:
        return FALLBACK_HEADER + "\n" + context

    content = (
        completion.choices[0].message.content
        if completion and completion.choices and completion.choices[0].message
        else None
    )
    if not content:
        return FALLBACK_HEADER + "\n" + context
    return content.strip()


def check_data(client: QdrantClient, config: Config) -> None:
    info = client.get_collection(config.collection)
    print(f"Collection: {config.collection}")
    print(f"Vectors count: {info.points_count}")
    points, _ = client.scroll(
        collection_name=config.collection,
        with_payload=True,
        limit=3,
    )
    if not points:
        print("No points found in the collection.")
        return
    print("Sample payloads:")
    for idx, point in enumerate(points, 1):
        payload_text = _payload_text(point.payload or {})
        suffix = "..." if len(payload_text) > 200 else ""
        print(f"{idx}. {payload_text[:200]}{suffix}")


def list_collections(client: QdrantClient) -> None:
    collections = client.get_collections()
    names = (
        [c.name for c in collections.collections]
        if collections and collections.collections
        else []
    )
    if not names:
        print("No collections found.")
        return
    print("Collections:")
    for name in names:
        print(f"- {name}")


def chat_loop(client: QdrantClient, groq_client: "OpenAI", config: Config) -> None:
    print("Book Chatbot (type 'exit' or 'quit' to leave)")
    while True:
        try:
            user_input = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            return

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            return

        try:
            query_vector = embed_query(user_input, config.embedding_model)
            points = search_qdrant(client, config, query_vector)
            if not points:
                print(NO_INFO_MESSAGE)
                continue
            context = build_context(points)
            if not context.strip():
                print(NO_INFO_MESSAGE)
                continue
            answer = ask_groq(user_input, context, groq_client, config.groq_model)
            print(answer)
        except Exception as exc:  # noqa: BLE001
            print(f"[error] {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Terminal chatbot using Qdrant + Gemini.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fetch a few sample points from Qdrant to verify data is present.",
    )
    parser.add_argument(
        "--list-collections",
        action="store_true",
        help="List available Qdrant collections.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        config = build_config()
        qdrant_client, groq_client = make_clients(config)
    except Exception as exc:  # noqa: BLE001
        print(f"[startup error] {exc}", file=sys.stderr)
        sys.exit(1)

    if args.check:
        check_data(qdrant_client, config)
        return

    if args.list_collections:
        list_collections(qdrant_client)
        return

    chat_loop(qdrant_client, groq_client, config)


if __name__ == "__main__":
    main()

