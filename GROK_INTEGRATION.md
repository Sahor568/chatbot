# Grok API Integration Guide

## Overview
Your chatbot now has **Grok AI integration** powered by xAI. This allows the chatbot to use intelligent AI responses with optional semantic search context.

## Features

### 1. **Grok Chat Endpoint** (`/chat`)
Direct chat with Grok AI without context.

**Request:**
```bash
POST /chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "What is FastAPI?"
    }
  ],
  "model": "grok-4-latest",
  "temperature": 0.7
}
```

**Response:**
```json
{
  "content": "FastAPI is a modern web framework for building APIs...",
  "model": "grok-4-latest",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50
  }
}
```

### 2. **RAG-Enhanced Chat** (`/chat-with-context`)
Combines semantic search with Grok AI for context-aware responses.

**Request:**
```bash
POST /chat-with-context
Content-Type: application/json

{
  "query": "How does FAISS work?",
  "messages": [
    {
      "role": "user",
      "content": "How does FAISS work?"
    }
  ]
}
```

**Response:**
```json
{
  "content": "FAISS is a library for efficient similarity search...",
  "model": "grok-4-latest",
  "context": ["FAISS is a library for efficient similarity search..."],
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 75
  }
}
```

### 3. **Semantic Search** (`/search`) - Original endpoint
Still available for traditional vector search without AI generation.

## Setup Instructions

### 1. Environment Configuration
Create/update `.env` file in the `backend/` directory:

```bash
GROK_API_KEY=your_api_key_here
```

**Note:** Get your API key from [console.x.ai](https://console.x.ai)

### 2. Install Dependencies
```bash
cd backend
pip install -r requirement.txt
```

The following packages are required:
- `requests` - HTTP client for API calls
- `python-dotenv` - Environment variable management
- `fastapi` - Web framework
- `uvicorn` - ASGI server

### 3. Start the Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m uvicorn main:app --reload --host 0.0.0.0
```

## Frontend Integration

The React frontend includes:
- **Toggle button** to switch between Grok AI and Semantic Search modes
- **Conversation history** passed to Grok for context
- **Error handling** with user-friendly messages
- **Loading state** with typing indicator

### Mode Switching
- **🤖 Grok AI**: Uses the Grok model with optional semantic context
- **🔍 Search**: Uses traditional semantic search with embeddings

## API Architecture

```
User Input (Frontend)
    ↓
[Grok Chat] ─────→ Grok API (https://api.x.ai/v1/chat/completions)
    ↑                    ↓
    └──────────────── JSON Response
    
[Grok + Context] ──→ FAISS Search (Retrieve relevant docs)
    ↓
    └──→ Combine context with Grok API
         Return enhanced response
```

## Troubleshooting

### "GROK_API_KEY not configured"
- Ensure `.env` file exists in `backend/` directory
- Verify the key is set correctly
- Restart the backend server after updating `.env`

### "Your team doesn't have credits"
- Visit [https://console.x.ai](https://console.x.ai)
- Purchase API credits for your team
- Make sure the API key belongs to an account with active credits

### Connection timeout
- Check your internet connection
- Verify firewall settings
- Ensure Grok API endpoint is accessible: `https://api.x.ai/v1/chat/completions`

## API Rate Limits
Grok API may have rate limits. Monitor usage in your [console.x.ai dashboard](https://console.x.ai).

## Model Options
- `grok-4-latest` - Latest Grok-4 model (recommended)
- `grok-latest` - Latest available Grok model

## Temperature Settings
- `0` - Deterministic, no randomness (best for testing)
- `0.7` - Balanced (default)
- `1.0` - More creative/random responses

## Example Usage

### JavaScript/Fetch
```javascript
// Grok Chat
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    messages: [{ role: 'user', content: 'Hello!' }],
    temperature: 0.7
  })
})

// RAG Chat
const response = await fetch('http://localhost:8000/chat-with-context', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'What is FastAPI?',
    messages: [{ role: 'user', content: 'What is FastAPI?' }]
  })
})
```

### Python/Requests
```python
import requests

response = requests.post(
    'http://localhost:8000/chat',
    json={
        'messages': [{'role': 'user', 'content': 'Hello!'}],
        'temperature': 0.7
    }
)
print(response.json())
```

## Security Notes
⚠️ **Important:**
- Never commit `.env` files to version control
- Add `.env` to `.gitignore`
- Rotate API keys if accidentally exposed
- Use environment variables in production

## Files Modified
- `backend/main.py` - Added `/chat` and `/chat-with-context` endpoints
- `backend/requirement.txt` - Added `requests` and `python-dotenv`
- `backend/.env` - API key configuration (create this file)
- `frontend/src/App.jsx` - Added Grok mode toggle and chat functionality
- `frontend/src/App.css` - Added styling for mode buttons

## Next Steps
1. ✅ Grok API is integrated
2. ⏳ Purchase API credits if needed
3. 🧪 Test with the frontend toggle
4. 📝 Monitor API usage in console.x.ai
5. 🚀 Deploy to production when ready
