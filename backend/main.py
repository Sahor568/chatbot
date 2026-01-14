from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# LangChain imports
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from typing import Optional, List, Any

# Load environment variables
load_dotenv()

from document import docs  # 👈 import docs

app = FastAPI()

# Configuration
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

# Pydantic models for request/response
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "grok-4-latest"
    temperature: float = 0.7

class ChatResponse(BaseModel):
    content: str
    model: str
    usage: dict = {}

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Custom LangChain LLM for Grok
# -----------------------------
class GrokLLM(LLM):
    """Custom LangChain LLM wrapper for Grok API"""
    
    model: str = "grok-4-latest"
    temperature: float = 0.7
    
    @property
    def _llm_type(self) -> str:
        return "grok"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """Call Grok API with the prompt"""
        if not GROK_API_KEY:
            return "Error: GROK_API_KEY not configured"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROK_API_KEY}"
        }
        
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": self.model,
            "stream": False,
            "temperature": self.temperature
        }
        
        try:
            response = requests.post(GROK_API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except requests.exceptions.RequestException as e:
            return f"Error calling Grok API: {str(e)}"

# -----------------------------
# Step 2: Load embedding model
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Step 3: Convert docs to embeddings
# -----------------------------
doc_embeddings = model.encode(docs)
doc_embeddings = np.array(doc_embeddings).astype("float32")

# -----------------------------
# Step 4: Create FAISS index (original)
# -----------------------------
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(doc_embeddings) # type: ignore

# -----------------------------
# Step 4b: LangChain Vector Store
# -----------------------------
langchain_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_text("\n".join(docs))
vectorstore = FAISS.from_texts(texts, langchain_embeddings)

# Initialize Grok LLM
grok_llm = GrokLLM()

# Create RAG chain
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}
Answer:"""

QA_PROMPT = PromptTemplate(
    template=template, input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=grok_llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    chain_type_kwargs={"prompt": QA_PROMPT}
)

# -----------------------------
# Step 5: Retrieval function
# -----------------------------
def retrieve(query: str, k: int = 2):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, k) # type: ignore

    return [docs[i] for i in indices[0]]

# -----------------------------
# Root test endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "jai mahakaal"}

# -----------------------------
# Step 6: Search API
# -----------------------------
@app.get("/search")
def search(query: str, k: int = 2):
    results = retrieve(query, k)
    return {
        "query": query,
        "results": results
    }

# -----------------------------
# Step 7: Grok Chat API
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    """Send a message to Grok AI"""
    if not GROK_API_KEY:
        return {"error": "GROK_API_KEY not configured"}
    
    # Prepare the request for Grok API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROK_API_KEY}"
    }
    
    payload = {
        "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
        "model": request.model,
        "stream": False,
        "temperature": request.temperature
    }
    
    try:
        response = requests.post(GROK_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "content": data.get("choices", [{}])[0].get("message", {}).get("content", ""),
            "model": data.get("model", "grok-4-latest"),
            "usage": data.get("usage", {})
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Grok API error: {str(e)}"}

# -----------------------------
# Step 8: LangChain RAG endpoint
# -----------------------------
@app.post("/chat-langchain")
def chat_langchain(query: str):
    """Use LangChain RAG chain to answer questions"""
    try:
        result = qa_chain.run(query)
        return {
            "query": query,
            "answer": result,
            "method": "langchain-rag"
        }
    except Exception as e:
        return {"error": f"LangChain error: {str(e)}"}

# -----------------------------
# Step 9: RAG-enhanced chat (Search + Grok)
# -----------------------------
@app.post("/chat-with-context")
def chat_with_context(query: str, messages: list[Message]):
    """Search documents and augment chat with context"""
    if not GROK_API_KEY:
        return {"error": "GROK_API_KEY not configured"}
    
    # Retrieve relevant documents
    relevant_docs = retrieve(query, k=2)
    context = "\n".join(relevant_docs)
    
    # Add context to messages
    system_message = f"You are a helpful assistant. Use the following context to answer questions:\n\n{context}"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROK_API_KEY}"
    }
    
    payload = {
        "messages": [
            {"role": "system", "content": system_message},
            *[{"role": msg.role, "content": msg.content} for msg in messages]
        ],
        "model": "grok-4-latest",
        "stream": False,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(GROK_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "content": data.get("choices", [{}])[0].get("message", {}).get("content", ""),
            "model": data.get("model", "grok-4-latest"),
            "context": relevant_docs,
            "usage": data.get("usage", {})
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Grok API error: {str(e)}"}