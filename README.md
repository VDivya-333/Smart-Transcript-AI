# 📝 Transcript Ingestion & Q&A System

A robust system designed to ingest conversation transcripts, process them using AI embeddings, and store them in a vector database for semantic search and retrieval. This project utilizes a Flask backend, a Streamlit frontend, Redis for job tracking, and ChromaDB for vector storage.

## 🚀 Features
- **Asynchronous Ingestion**: Jobs are queued and processed in background threads.
- **Semantic Search**: Uses `SentenceTransformers` (`all-MiniLM-L6-v2`) to generate embeddings for transcript chunks.
- **Vector Storage**: Stores and queries data using `ChromaDB`.
- **Job Management**: Uses `Redis` to track job statuses (QUEUED, INJECTING_DATA, COMPLETED, FAILED).
- **Interactive UI**: A multi-tab Streamlit application for uploading, monitoring, and querying.
- **API Documentation**: Built-in Swagger UI for exploring the REST API.

## 🏗️ Architecture
- **Backend**: Flask (Python)
- **Frontend**: Streamlit
- **Task Tracking**: Redis
- **Vector Database**: ChromaDB
- **ML Model**: SentenceTransformers

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Redis Server (Running on localhost:6379 by default)

### 1. Install Dependencies
```bash
pip install flask flasgger redis sentence-transformers chromadb requests streamlit python-dotenv werkzeug
```

### 2. Configuration
Create a `.env` file in the root directory (if not already present):
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### 3. Run the Application
You need to run two separate processes:

**Start the Flask Backend:**
```bash
python run.py
```
*The API will be available at `http://127.0.0.1:5000` and Swagger docs at `http://127.0.0.1:5000/docs`.*

**Start the Streamlit Frontend:**
```bash
streamlit run streamlit_app.py
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/upload` | `POST` | Upload a JSON transcript file to the server. |
| `/ingest` | `POST` | Queue a background job to process a transcript URL. |
| `/status/<job_id>` | `GET` | Check the status and see the output of a job. |
| `/query` | `POST` | Ask a question against a specific `transcript_id`. |
| `/docs` | `GET` | Interactive Swagger API documentation. |

## 📖 How to Use

1.  **Upload & Ingest**:
    - Open the Streamlit UI.
    - Use **Tab 1** to upload your JSON file. 
    - Once uploaded, click "Start Ingesting" to begin the background embedding process.
2.  **Monitor Progress**:
    - Switch to **Tab 2**.
    - Enter your Job ID (Transcript ID) to see if the processing is `QUEUED`, `INJECTING_DATA`, or `COMPLETED`.
3.  **Ask Questions**:
    - Go to **Tab 3**.
    - Enter the Transcript ID and your question.
    - The system will retrieve the most relevant segments from that specific conversation.

## 📄 License
MIT