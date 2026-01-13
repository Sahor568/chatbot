from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from document import docs  # 👈 import docs

app = FastAPI()

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
# Step 4: Create FAISS index
# -----------------------------
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(doc_embeddings) # type: ignore

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
    return {"message": "Hare Krishna"}

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