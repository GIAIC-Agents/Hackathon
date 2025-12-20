from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API routers
from src.api import rag
from src.core.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Docusaurus RAG Chatbot API",
    description="REST API for the Docusaurus RAG Chatbot Integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Docusaurus dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(rag.router, prefix="/api", tags=["rag"])

@app.get("/")
def read_root():
    return {"message": "Docusaurus RAG Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)