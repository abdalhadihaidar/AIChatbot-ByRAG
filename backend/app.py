import os
import subprocess  # To run LLaMA via command line
from bs4 import BeautifulSoup
import faiss
import numpy as np
from flask import Flask, request, jsonify
import requests
from werkzeug.utils import secure_filename
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from llama_index.core import SimpleDirectoryReader

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Directory paths
UPLOAD_FOLDER = './backend/data/documents'
VECTOR_STORE_DIR = './backend/vector_store/'
FAISS_INDEX_FILE = os.path.join(VECTOR_STORE_DIR, 'index.faiss')

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the pre-trained embedding model (for query embeddings)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# -------------------
# Helper Functions
# -------------------

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to load FAISS index from disk
def load_faiss_index():
    if not os.path.exists(FAISS_INDEX_FILE):
        raise ValueError(f"FAISS index not found at {FAISS_INDEX_FILE}")
    print(f"FAISS index loaded from: {FAISS_INDEX_FILE}")
    return faiss.read_index(FAISS_INDEX_FILE)

# Function to query the FAISS index and retrieve relevant documents
def query_faiss_index(query, top_k=5):
    index = load_faiss_index()

    # Convert the user's query into an embedding
    query_embedding = embedder.encode([query], convert_to_tensor=False)
    query_embedding = np.array(query_embedding).astype('float32')

    # Perform similarity search
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve document contents based on FAISS indices
    reader = SimpleDirectoryReader(UPLOAD_FOLDER)
    documents = reader.load_data()
    retrieved_docs = [documents[i].text for i in indices[0]]  # Get the actual document content based on FAISS indices
    
    print(f"Query: {query}")
    print(f"Retrieved documents (top {top_k}): {retrieved_docs}")

    return retrieved_docs

# Function to generate answers using LLaMA via command line
def generate_answer_llama(query, context):
    combined_input = f"Question: {query}\nContext: {context}\nAnswer:"
    llama_command = f'ollama run llama3.1'

    print(f"Sending combined input to LLaMA:\n{combined_input}")

    try:
        # Use subprocess to run the ollama command and send the input
        result = subprocess.run(
            llama_command, 
            input=combined_input.encode('utf-8'),  # Encode the input as UTF-8
            shell=True,
            capture_output=True,
            text=False  # We will handle text decoding manually
        )

        # Check if the command failed
        if result.returncode != 0:
            raise Exception(f"LLaMA command failed: {result.stderr.decode('utf-8')}")  # Decode stderr as UTF-8

        # Capture and return the LLaMA output from stdout, decode as UTF-8
        answer = result.stdout.decode('utf-8').strip()
        print(f"LLaMA returned answer: {answer}")
        return answer

    except Exception as e:
        print(f"Error generating answer: {e}")
        return f"Error generating answer: {str(e)}"


# -------------------
# Upload Endpoints
# -------------------

# File Upload Endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            print("No file part in the request")
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        
        if file.filename == '':
            print("No selected file")
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
                print(f"Created folder: {app.config['UPLOAD_FOLDER']}")

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            print(f"File saved at: {file_path}")

            return jsonify({"message": "File uploaded successfully"}), 200
        else:
            print("File type not allowed")
            return jsonify({"error": "File type not allowed"}), 400

    except Exception as e:
        print(f"Error during file upload: {e}")
        return jsonify({"error": str(e)}), 500
# Text Upload Endpoint
@app.route('/upload-text', methods=['POST'])
def upload_text():
    try:
        data = request.get_json()
        text_content = data.get('text')

        if not text_content:
            return jsonify({"error": "No text provided"}), 400

        # Save text to a file
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_text.txt')
        with open(file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text_content)

        print(f"Text content saved to: {file_path}")
        return jsonify({"message": "Text uploaded successfully"}), 200
    except Exception as e:
        print(f"Error during text upload: {e}")
        return jsonify({"error": str(e)}), 500


# Q&A Upload Endpoint
@app.route('/upload-qa', methods=['POST'])
def upload_qa():
    try:
        data = request.get_json()
        question = data.get('question')
        answer = data.get('answer')

        if not question or not answer:
            return jsonify({"error": "Both question and answer are required"}), 400

        # Save Q&A to a file
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'qa_pairs.txt')
        with open(file_path, 'a', encoding='utf-8') as qa_file:
            qa_file.write(f"Q: {question}\nA: {answer}\n\n")

        print(f"Q&A saved to: {file_path}")
        return jsonify({"message": "Q&A uploaded successfully"}), 200
    except Exception as e:
        print(f"Error during Q&A upload: {e}")
        return jsonify({"error": str(e)}), 500


# Website URL Upload Endpoint
@app.route('/upload-website', methods=['POST'])
def upload_website():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Fetch website content
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        website_content = soup.get_text()

        # Save website content to a file
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'website_content.txt')
        with open(file_path, 'w', encoding='utf-8') as website_file:
            website_file.write(website_content)

        print(f"Website content saved to: {file_path}")
        return jsonify({"message": "Website content uploaded successfully"}), 200
    except Exception as e:
        print(f"Error during website upload: {e}")
        return jsonify({"error": str(e)}), 500

# -------------------
# Query and Answer Generation using FAISS and LLaMA
# -------------------

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        user_query = data.get('query')

        if not user_query:
            print("No query provided")
            return jsonify({"error": "No query provided"}), 400

        # Step 1: Retrieve relevant documents using FAISS
        retrieved_docs = query_faiss_index(user_query, top_k=5)
        context = " ".join(retrieved_docs)  # Combine all retrieved documents as the context

        # Step 2: Generate an answer using LLaMA with the retrieved documents as context
        answer = generate_answer_llama(user_query, context)

        return jsonify({
            "query": user_query,
            "results": {
                "answer": answer,
                "documents": retrieved_docs
            }
        }), 200
    except Exception as e:
        print(f"Error during query processing: {e}")
        return jsonify({"error": str(e)}), 500

# -------------------
# Health Check Endpoint
# -------------------
@app.route('/health', methods=['GET'])
def health_check():
    print("Health check requested")
    return jsonify({"status": "running"}), 200

# Run the Flask app
if __name__ == '__main__':
    print("Starting Flask app on http://localhost:5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)