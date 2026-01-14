# Chatbot Application

A modern AI-powered chatbot with a React frontend and FastAPI backend using semantic search with embeddings.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)

## 🤖 Overview

This chatbot application combines:
- **Frontend**: Modern React UI with real-time message display
- **Backend**: FastAPI with semantic search using embeddings and FAISS indexing
- **Features**: Document retrieval, real-time chat interface, responsive design

## 📦 Prerequisites

### System Requirements
- Python 3.8 or higher
- Node.js 16+ and npm
- 10GB free disk space (for PyTorch and dependencies)
- Linux/macOS or Windows with WSL

### Tools
- Git (for version control)
- Python pip (package manager)
- npm (Node.js package manager)

## 🗂️ Project Structure

```
chatbot/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── document.py          # Document data
│   ├── requirement.txt       # Python dependencies
│   └── venv/               # Virtual environment (created after setup)
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Styles
│   │   └── main.jsx        # Entry point
│   ├── public/             # Static assets
│   ├── package.json        # npm dependencies
│   └── vite.config.js      # Vite configuration
├── README.md               # This file
└── SETUP_GUIDE.md          # Detailed setup guide
```

## 🚀 Installation

### Step 1: Clone or Navigate to Project

```bash
cd /home/mrrv/research/chatbot
```

### Step 2: Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a Python virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate  # On Windows
```

Install Python dependencies:

```bash
pip install -r requirement.txt
```

**Note**: This may take 10-15 minutes due to PyTorch installation (~5GB).

### Step 3: Frontend Setup

In a new terminal, navigate to the frontend directory:

```bash
cd frontend
```

Install npm dependencies:

```bash
npm install
```

## ⚡ Quick Start

### Option 1: Terminal Approach (Recommended)

**Terminal 1 - Backend:**
```bash
cd /home/mrrv/research/chatbot/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0
```

**Terminal 2 - Frontend:**
```bash
cd /home/mrrv/research/chatbot/frontend
npm run dev
```

### Option 2: One-Command Approach

**Terminal 1 - Backend:**
```bash
cd /home/mrrv/research/chatbot/backend && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0
```

**Terminal 2 - Frontend:**
```bash
cd /home/mrrv/research/chatbot/frontend && npm run dev
```

## 🎮 Usage

1. **Start Backend Service**
   - Navigate to backend directory
   - Activate virtual environment
   - Run `uvicorn main:app --reload --host 0.0.0.0`
   - Backend will be available at `http://localhost:8000`

2. **Start Frontend Service**
   - Navigate to frontend directory
   - Run `npm run dev`
   - Frontend will be available at `http://localhost:5173`

3. **Access the Application**
   - Open your browser
   - Navigate to `http://localhost:5173`
   - Start typing messages in the chat interface
   - Frontend sends queries to backend
   - Responses appear in real-time

## 🏗️ Architecture

### Backend Architecture

- **Framework**: FastAPI
- **Search Engine**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Endpoints**:
  - `GET /` - Health check
  - `GET /search?query=<query>&k=2` - Search documents
- **CORS**: Enabled for localhost:5173

### Frontend Architecture

- **Framework**: React 19
- **Build Tool**: Vite
- **Features**:
  - Real-time message display
  - Typing indicator
  - Auto-scroll to latest messages
  - Responsive design
  - Message timestamps

### Data Flow

```
User Input
    ↓
React Component (App.jsx)
    ↓
HTTP GET Request to /search
    ↓
FastAPI Backend (main.py)
    ↓
FAISS Index Search
    ↓
Document Retrieval
    ↓
JSON Response
    ↓
React Display
```

## 🔍 API Endpoints

### Health Check
```bash
curl http://localhost:8000/
```

Response:
```json
{
  "message": "jai mahakaal"
}
```

### Search Documents
```bash
curl "http://localhost:8000/search?query=your+query&k=2"
```

Parameters:
- `query` (string): Search query
- `k` (integer, default=2): Number of results to return

Response:
```json
{
  "query": "your query",
  "results": ["document1", "document2"]
}
```

## 📝 Available Commands

### Backend Commands

```bash
# Start development server with auto-reload
uvicorn main:app --reload --host 0.0.0.0

# Start production server
uvicorn main:app --host 0.0.0.0 --port 8000

# Run with different port
uvicorn main:app --port 8001
```

### Frontend Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run ESLint
npm run lint
```

## 🐛 Troubleshooting

### Backend Issues

**Problem**: "Port 8000 already in use"
```bash
# Use a different port
uvicorn main:app --reload --port 8001
# Then update frontend API URL in App.jsx
```

**Problem**: "No module named 'torch'"
```bash
# Reinstall dependencies
pip install -r requirement.txt --no-cache-dir
```

**Problem**: "ModuleNotFoundError: No module named 'document'"
```bash
# Ensure you're in the backend directory
# Check that document.py exists
ls -la backend/document.py
```

### Frontend Issues

**Problem**: "Port 5173 already in use"
```bash
npm run dev -- --port 5174
```

**Problem**: "Cannot find module 'react'"
```bash
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Backend not responding
```bash
# Check if backend is running
curl http://localhost:8000/

# If not, start backend in separate terminal
cd backend && source venv/bin/activate && uvicorn main:app --reload
```

### General Issues

**Problem**: "Connection refused"
- Ensure backend is running on port 8000
- Ensure frontend is running on port 5173
- Check firewall settings

**Problem**: Long installation time
- PyTorch is ~5GB, initial installation takes time
- Ensure you have stable internet connection
- Consider using `--no-cache-dir` flag with pip

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Sentence Transformers](https://www.sbert.net/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)

## 📄 Configuration Files

- `backend/requirement.txt` - Python dependencies
- `frontend/package.json` - Node.js dependencies
- `frontend/vite.config.js` - Vite configuration
- `frontend/.eslintrc.js` - ESLint configuration

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

---

**Last Updated**: January 14, 2026
