import os
import faiss
import numpy as np
from llama_index.core.node_parser import SimpleFileNodeParser
from llama_index.core import SimpleDirectoryReader
from sentence_transformers import SentenceTransformer

from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,ServiceContext,PromptTemplate


# Directory paths
DOCUMENTS_DIR = 'backend/data/documents/'  # Where documents (PDF, CSV, TXT) are stored
VECTOR_STORE_DIR = './backend/vector_store/'  # Where FAISS index will be stored
FAISS_INDEX_FILE = os.path.join(VECTOR_STORE_DIR, 'index.faiss')

# Load a local embedding model (instead of OpenAI)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Function to process documents and convert them to embeddings
def process_documents():
    # Initialize the list for storing document texts
    all_documents = []

    # Load and process all files in the DOCUMENTS_DIR
    for filename in os.listdir(DOCUMENTS_DIR):
        file_path = os.path.join(DOCUMENTS_DIR, filename)
        
        # Check file type and process accordingly
        if filename.endswith('.txt') or filename.endswith('.csv') or filename.endswith('.pdf'):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                all_documents.append(content)
                print(f"Processed file: {filename}")
        else:
            print(f"Skipping unsupported file: {filename}")
    
    # Ensure we have documents to index
    if not all_documents:
        raise ValueError("No documents found for indexing!")

    # Convert documents to embeddings using the local model
    document_texts = all_documents
    embeddings = embedder.encode(document_texts, convert_to_tensor=False)
    embeddings = np.array(embeddings).astype('float32')

    # Create a vector index using FAISS for efficient similarity search
    dimension = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)  # L2 (Euclidean) distance index
    faiss_index.add(embeddings)  # Add embeddings to the FAISS index

    # Save FAISS index to disk
    if not os.path.exists(VECTOR_STORE_DIR):
        os.makedirs(VECTOR_STORE_DIR)
    faiss.write_index(faiss_index, FAISS_INDEX_FILE)

    print(f"Indexed {len(embeddings)} documents and stored the index in {FAISS_INDEX_FILE}")

# Run the ingestion process
if __name__ == "__main__":
    process_documents()