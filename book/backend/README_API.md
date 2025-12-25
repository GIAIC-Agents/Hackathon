# Book Chatbot API Server

FastAPI server that wraps the `chatbot.py` logic for web API access.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your `.env` file has the required variables:
- `GEMINI_API_KEY`
- `GROQ_API_KEY`
- `QDRANT_URL` or `QDRANT_ENDPOINT`
- `QDRANT_API_KEY`
- `QDRANT_COLLECTION`

## Running the Server

```bash
python api_server.py
```

Or with uvicorn directly:
```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /api/rag/health
```

### Query Endpoint
```
POST /api/rag/query
Content-Type: application/json

{
  "query": "your question here",
  "session_id": "optional-session-id"
}
```

Response:
```json
{
  "response": "AI generated answer",
  "sources": ["source1", "source2"],
  "session_id": "optional-session-id"
}
```

## Frontend Connection

The Docusaurus frontend in the `book` folder is configured to connect to `http://localhost:8000/api/rag/query` by default.

To change the API URL, set the `DOCUSAURUS_API_BASE_URL` environment variable when running the frontend.

