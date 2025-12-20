import google.generativeai as genai
import logging
import asyncio
from typing import List
from src.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. Gemini service may not function correctly.")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.embedding_model = "models/embedding-001"

    async def generate_response(self, query: str, context: str) -> str:
        """
        Generate a response using Gemini based on the query and context
        """
        try:
            logger.info("Generating response using Gemini")
            
            # Construct the prompt with context
            prompt = f"""
            You are an expert assistant. Answer the user's question strictly using only the information provided in the given context retrieved from the Qdrant vector database. Do not use any external knowledge, assumptions, or prior training data. If the answer cannot be clearly derived from the provided context, explicitly state that the available documents do not contain sufficient information to answer the question. Ensure the response is clear, accurate, and easy to understand, and present the information in a concise and well-structured manner without adding anything beyond the given context.

            Context:
            {context}
            
            Question: {query}
            
            Answer:
            """
            
            # Gemini generation
            response = self.model.generate_content(prompt)
            
            if response.text:
                answer = response.text.strip()
                logger.info("Response generated successfully")
                return answer
            else:
                logger.warning("Gemini returned empty response")
                return "I apologize, but I couldn't generate a response."
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    async def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for the given text using Gemini with retry logic
        """
        max_retries = 5
        base_delay = 10
        
        for attempt in range(max_retries):
            try:
                # Gemini embedding generation
                # Note: models/embedding-001 returns 768 dimensions
                result = await asyncio.to_thread(
                    genai.embed_content,
                    model=self.embedding_model,
                    content=text,
                    task_type="retrieval_query"
                )
                
                embedding = result['embedding']
                logger.info(f"Generated embedding with {len(embedding)} dimensions")
                return embedding
                
            except Exception as e:
                error_msg = str(e)
                if "Quota exceeded" in error_msg or "429" in error_msg:
                    delay = base_delay * (attempt + 1)
                    if "retry in" in error_msg:
                        # Extract seconds if possible, or use default long delay
                        # For simplicity, using 60s as free tier limit is usually per minute
                        delay = 65
                    
                    logger.warning(f"Rate limit hit. Retrying in {delay} seconds... (Attempt {attempt+1}/{max_retries})")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Error generating embedding: {str(e)}")
                    raise
        
        raise Exception("Failed to generate embedding after max retries")
