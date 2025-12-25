"""
FastAPI server that wraps the chatbot.py logic for web API access.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import logging

# Import chatbot functions
from chatbot import (
    build_config,
    make_clients,
    embed_query,
    search_qdrant,
    build_context,
    ask_groq,
    NO_INFO_MESSAGE,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global clients (initialized on startup)
config = None
qdrant_client = None
groq_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    global config, qdrant_client, groq_client
    try:
        logger.info("Initializing chatbot clients...")
        config = build_config()
        qdrant_client, groq_client = make_clients(config)
        logger.info("Chatbot clients initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize chatbot clients: {e}")
        raise
    
    yield
    
    # Shutdown (if needed in the future)
    logger.info("Shutting down chatbot service...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Book Chatbot API",
    description="REST API for the Book Chatbot using Qdrant and Groq",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    response: str
    sources: Optional[list] = None
    session_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Book Chatbot API is running"}


@app.get("/api/rag/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="1.0.0")


@app.options("/api/rag/query")
async def options_query():
    """Handle CORS preflight requests."""
    return {"message": "OK"}


@app.post("/api/rag/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Process a user query using the RAG pipeline.
    """
    global config, qdrant_client, groq_client
    
    logger.info(f"Received query request: {request.query}")
    
    if not config or not qdrant_client or not groq_client:
        logger.error("Chatbot service not initialized")
        raise HTTPException(
            status_code=503,
            detail="Chatbot service not initialized. Please check server logs."
        )
    
    try:
        logger.info(f"Processing query: {request.query}")
        
        # Step 1: Generate embedding for the query
        query_vector = embed_query(request.query, config.embedding_model)
        
        # Step 2: Search Qdrant for relevant documents
        points = search_qdrant(qdrant_client, config, query_vector)
        
        if not points:
            return QueryResponse(
                response=NO_INFO_MESSAGE,
                sources=[],
                session_id=request.session_id
            )
        
        # Step 3: Build context from retrieved documents
        context = build_context(points)
        
        if not context.strip():
            return QueryResponse(
                response=NO_INFO_MESSAGE,
                sources=[],
                session_id=request.session_id
            )
        
        # Step 4: Generate response using Groq
        answer = ask_groq(request.query, context, groq_client, config.groq_model)
        
        logger.info("Response generated successfully")
        
        # Extract sources from points
        sources = []
        for point in points:
            if point.payload:
                source = point.payload.get("source") or point.payload.get("file") or "Unknown"
                sources.append(str(source))
        
        return QueryResponse(
            response=answer,
            sources=sources if sources else None,
            session_id=request.session_id
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return QueryResponse(
            response="I apologize, but I'm having trouble processing your request right now. Please try again in a moment.",
            sources=[],
            session_id=request.session_id
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

