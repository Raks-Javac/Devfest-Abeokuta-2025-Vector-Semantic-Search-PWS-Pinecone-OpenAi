# DevFest Abeokuta 2025 - Vector Semantic Search Demo

A complete demonstration of semantic vector search using OpenAI embeddings, Pinecone vector database, and FastAPI.

## 🚀 Features

- 🔍 **Semantic Search**: Natural language queries with vector similarity
- 🤖 **OpenAI Embeddings**: text-embedding-3-large (3072 dimensions)
- 📊 **Pinecone Vector DB**: Scalable, production-ready vector storage
- 🌐 **RESTful API**: FastAPI backend with automatic documentation
- 📚 **Dataset Support**: Load and index Hugging Face datasets
- 🐳 **Docker Ready**: Containerized for easy deployment
- ☁️ **Render Deployment**: One-click deployment configuration

## Project Structure

```
├── src/
│   ├── vector_demo.py           # Standalone demo: embedding → index → query
│   └── requirements.txt
│
├── backend/
│   ├── app/
│   │   ├── config.py             # Configuration management
│   │   ├── models.py             # Pydantic request/response models
│   │   ├── routes.py             # API endpoints
│   │   ├── search_service.py     # Vector search logic
│   │   └── __init__.py
│   ├── main.py                   # FastAPI application
│   ├── requirements.txt
│   ├── Dockerfile                # Docker configuration
│   ├── .dockerignore
│   └── README.md
│
├── render.yaml                   # Render deployment config
├── .env                          # Environment variables (not in git)
└── README.md
```

## 🛠️ Technologies Used

### Backend

- **FastAPI**: Modern, fast web framework for building APIs
- **OpenAI API**: Text embedding generation (text-embedding-3-large)
- **Pinecone**: Serverless vector database
- **Datasets**: Hugging Face datasets library
- **NumPy**: Numerical operations for similarity calculations
- **Pydantic**: Data validation and settings management

### Deployment

- **Docker**: Containerization
- **Render**: Cloud deployment platform
- **Uvicorn**: ASGI server

## 📋 Prerequisites

- Python 3.9+
- OpenAI API key
- Pinecone API key
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd devfest_abk_2025_vector_semantic_

# Create and activate virtual environment
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

### 2. Environment Variables

Create a `.env` file in the project root:

```env
# Required API Keys
PINECONE_API_KEY=your_pinecone_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Standalone Demo

```bash
cd src
pip install -r requirements.txt
python vector_demo.py
```

### 4. Run the Backend API

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API will be available at:

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 Docker Deployment

### Build and Run Locally

```bash
cd backend

# Build the image
docker build -t vector-search-api .

# Run the container
docker run -p 8000:8000 \
  -e PINECONE_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  vector-search-api
```

## ☁️ Deploy to Render

### Option 1: Using render.yaml (Recommended)

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml`
6. Add environment variables:
   - `PINECONE_API_KEY`
   - `OPENAI_API_KEY`
7. Click "Apply" to deploy!

### Option 2: Manual Deployment

1. Create a new **Web Service** on Render
2. Connect your GitHub repository
3. Configure:
   - **Name**: vector-search-api
   - **Environment**: Docker
   - **Dockerfile Path**: `./backend/Dockerfile`
   - **Docker Context**: `./backend`
4. Add environment variables
5. Deploy!

## 📚 API Endpoints

### Health & Configuration

- `GET /health` - Health check with API key validation
- `GET /config` - Configuration information

### Embeddings

- `POST /api/embeddings/create` - Generate embeddings from text
- `POST /api/embeddings/similarity` - Calculate similarity between texts

### Index Management

- `GET /api/indexes/list` - List all Pinecone indexes
- `POST /api/indexes/create` - Create new vector index
- `GET /api/indexes/{index_name}/stats` - Get index statistics

### Dataset Operations

- `POST /api/dataset/load` - Load dataset from Hugging Face
- `POST /api/dataset/index` - Index dataset into Pinecone

### Search

- `POST /api/search` - Perform semantic search

## 💡 Usage Examples

### Create Embeddings

```bash
curl -X POST http://localhost:8000/api/embeddings/create \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Hello world", "Vector search is powerful"]}'
```

### Semantic Search

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a beehive?", "top_k": 3}'
```

### Calculate Similarity

```bash
curl -X POST http://localhost:8000/api/embeddings/similarity \
  -H "Content-Type: application/json" \
  -d '{"text1": "The tap is dripping", "text2": "We need a plumber"}'
```

## 🔧 Development

### Project Components

1. **vector_demo.py**: Standalone demonstration of the complete workflow

   - Embedding generation
   - Similarity calculations
   - Dataset loading
   - Vector indexing
   - Semantic search

2. **Backend API**: Production-ready FastAPI service
   - RESTful endpoints
   - Request validation
   - Error handling
   - Interactive documentation

### Running Tests

```bash
cd backend
pytest
```

### Code Formatting

```bash
black .
```

## 📖 Documentation

- **Backend API Docs**: See [backend/README.md](backend/README.md)
- **Interactive API Docs**: http://localhost:8000/docs (when running)
- **Standalone Demo**: See comments in `src/vector_demo.py`

## 🤝 Contributing

This is a demo project for DevFest Abeokuta 2025. Feel free to fork and extend!

## 📝 License

MIT License - DevFest Abeokuta 2025

## 🙏 Acknowledgments

- OpenAI for embeddings API
- Pinecone for vector database
- FastAPI for the web framework
- Hugging Face for datasets

## 📧 Contact

For questions or feedback about this demo, please reach out during DevFest Abeokuta 2025!
