import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Directory paths
VECTOR_STORE_DIR = './backend/vector_store/'
FAISS_INDEX_FILE = os.path.join(VECTOR_STORE_DIR, 'index.faiss')

# Load the pre-trained embedding model (you can use a smaller model here)
embedder = SentenceTransformer('all-MiniLM-L6-v2')  # A lightweight model for generating query embeddings

# Function to load the FAISS index from disk
def load_faiss_index():
    if not os.path.exists(FAISS_INDEX_FILE):
        raise ValueError(f"FAISS index not found at {FAISS_INDEX_FILE}")
    
    # Load FAISS index from file
    index = faiss.read_index(FAISS_INDEX_FILE)
    return index

# Function to query the FAISS index and retrieve relevant documents
def query_faiss_index(query, top_k=5):
    # Load FAISS index
    index = load_faiss_index()

    # Convert the user query into an embedding using SentenceTransformer
    query_embedding = embedder.encode([query], convert_to_tensor=False)
    query_embedding = np.array(query_embedding).astype('float32')

    # Perform a similarity search using FAISS
    distances, indices = index.search(query_embedding, top_k)
    
    return indices, distances

# Example usage
if __name__ == "__main__":
    # Example query from the user
    user_query = "What is the capital of France?"

    # Retrieve top 5 similar documents
    indices, distances = query_faiss_index(user_query, top_k=5)

    print(f"Top documents for query '{user_query}':")
    print(f"Indices: {indices}")
    print(f"Distances: {distances}")
