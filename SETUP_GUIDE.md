# Chatbot Setup Guide

## Frontend Setup

### Prerequisites
- Node.js 16+ installed
- npm or yarn package manager

### Installation & Running

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:5173` (or another port if 5173 is busy)

### Features
- Modern chat interface with gradient design
- Real-time message display with timestamps
- Typing indicator animation
- Responsive design for mobile and desktop
- Auto-scroll to latest messages
- Disabled send button while loading

---

## Backend Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Installation & Running

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirement.txt
```

3. Start the FastAPI server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload
```

The backend will start on `http://localhost:8000`

---

## API Endpoints

### Search Endpoint
- **URL**: `http://localhost:8000/search`
- **Method**: GET
- **Parameters**:
  - `query` (string): The search query
  - `k` (integer, optional): Number of results to return (default: 2)
- **Response**:
```json
{
  "query": "your query",
  "results": ["result 1", "result 2"]
}
```

### Root Endpoint
- **URL**: `http://localhost:8000/`
- **Method**: GET
- **Response**:
```json
{
  "message": "jai mahakaal"
}
```

---

## Running Both Services

In separate terminal windows:

**Terminal 1 - Backend**:
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

Then open your browser to the frontend URL (e.g., `http://localhost:5173`)

---

## Troubleshooting

### CORS Issues
If you get CORS errors, update the backend to allow requests from the frontend:

In `backend/main.py`, add:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Connection Refused
Make sure both the frontend and backend are running on their respective ports before trying to use the chatbot.

---

## Technology Stack

**Frontend**:
- React 18
- Vite
- CSS3 (No external CSS framework)

**Backend**:
- FastAPI
- Sentence Transformers
- FAISS (Vector database)
- NumPy
