from pydantic_settings import SettingsConfigDict, BaseSettings
import os
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Application settings
    APP_NAME: str = "Docusaurus RAG Chatbot API"
    APP_VERSION: str = "1.0.0"
    
    # Qdrant settings
    QDRANT_URL: str = "https://b3d322b2-6c79-4854-b2e8-b7941ec42f65.us-east4-0.gcp.cloud.qdrant.io:6333"
    QDRANT_API_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ukKXDAD040ermRRcD-BFIdb_mI8kHmWJQnF5JfMri8Q"
    QDRANT_COLLECTION_NAME: str = "book_embeddings"
    
    # Neon Postgres settings
    NEON_DATABASE_URL: str = ""
    
    # OpenAI settings
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Gemini settings
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-pro"
    
    # Other settings
    CORS_ORIGINS: str = "*"


settings = Settings()