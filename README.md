# DevFest Abeokuta 2025 - Vector Semantic Search Demo

A complete demonstration of semantic vector search using embeddings, vector indexing, and similarity queries.

## Project Structure

```
├── src/
│   └── vector_demo.py           # Standalone demo: embedding → index → query
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entrypoint
│   │   ├── search_service.py    # Core logic
│   │   └── __init__.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── lib/
│   │   └── main.dart            # Simple Flutter UI for queries
│   ├── pubspec.yaml
│   └── README.md
│
├── resources/
│   ├── dataset_info.md          # Notes or link to dataset used
│   ├── vector_visuals.png       # Optional diagrams
│   └── references.md            # Docs & articles
│
├── .env                         # Template for API keys
└── README.md
```

## Setup

### Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

## Quick Start

### 1. Standalone Demo
```bash
cd src
python vector_demo.py
```

### 2. Backend API
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Frontend UI
```bash
cd frontend
flutter pub get
flutter run
```

## Features

- 🔍 Semantic vector search
- 🚀 Fast similarity queries using FAISS
- 🌐 RESTful API with FastAPI
- 📱 Cross-platform Flutter UI
- 🎯 Easy-to-understand demo code

## Technologies Used

- **Backend**: Python, FastAPI, FAISS, Sentence Transformers
- **Frontend**: Flutter/Dart
- **Vector Search**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: Sentence Transformers

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# API Keys
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx
PINECONE_API_KEY=your-pinecone-api-key-here

# Backend Configuration
BACKEND_HOST=localhost
BACKEND_PORT=8000

# Database/Vector Store
VECTOR_DB_PATH=./data/vector_index

# Model Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Note**: Never commit your actual `.env` file to version control. The `.gitignore` file is configured to exclude it.

## Contributing

This is a demo project for DevFest Abeokuta 2025. Feel free to fork and extend!

## Resources

See `resources/references.md` for additional documentation and learning materials.
