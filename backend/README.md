# Backend - Vector Search API

FastAPI-based backend for semantic vector search using OpenAI embeddings and Pinecone vector database.

## Features

- 🔍 **Semantic Search**: Query using natural language
- 🤖 **OpenAI Embeddings**: text-embedding-3-large model (3072 dimensions)
- 📊 **Pinecone Integration**: Scalable vector database
- 📚 **Dataset Support**: Load and index Hugging Face datasets
- 🚀 **Fast API**: RESTful endpoints with automatic documentation
- 🐳 **Docker Ready**: Containerized for easy deployment

## Quick Start

### Local Development

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
   Create a `.env` file in the project root:

```env
PINECONE_API_KEY=your_pinecone_api_key
OPENAI_API_KEY=your_openai_api_key
```

3. **Run the server:**

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Docker

1. **Build the image:**

```bash
docker build -t vector-search-api .
```

2. **Run the container:**

```bash
docker run -p 8000:8000 \
  -e PINECONE_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  vector-search-api
```

## API Endpoints

### Health & Configuration

- `GET /health` - Health check with API key validation
- `GET /config` - Configuration information

### Embeddings

- `POST /api/embeddings/create` - Generate embeddings from text
- `POST /api/embeddings/similarity` - Calculate text similarity

### Index Management

- `GET /api/indexes/list` - List all Pinecone indexes
- `POST /api/indexes/create` - Create new vector index
- `GET /api/indexes/{index_name}/stats` - Get index statistics

### Dataset Operations

- `POST /api/dataset/load` - Load dataset from Hugging Face
- `POST /api/dataset/index` - Index dataset into Pinecone

### Search

- `POST /api/search` - Perform semantic search

## API Documentation

Interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Usage Examples

### Create Embeddings

```bash
curl -X POST http://localhost:8000/api/embeddings/create \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Hello world", "Vector search"]}'
```

### Semantic Search

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a beehive?", "top_k": 3}'
```

### Load Dataset

```bash
curl -X POST http://localhost:8000/api/dataset/load \
  -H "Content-Type: application/json" \
  -d '{"dataset_name": "squad_v2", "split": "train", "preview_count": 5}'
```

## Deployment to Render

### Option 1: Using render.yaml (Recommended)

1. Push your code to GitHub
2. Connect your repository to Render
3. Render will automatically detect `render.yaml` and deploy
4. Add environment variables in Render dashboard:
   - `PINECONE_API_KEY`
   - `OPENAI_API_KEY`

### Option 2: Manual Deployment

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Environment**: Docker
   - **Dockerfile Path**: `./backend/Dockerfile`
   - **Docker Context**: `./backend`
4. Add environment variables
5. Deploy!

## Environment Variables

| Variable           | Description                 | Required |
| ------------------ | --------------------------- | -------- |
| `PINECONE_API_KEY` | Pinecone API key            | Yes      |
| `OPENAI_API_KEY`   | OpenAI API key              | Yes      |
| `PORT`             | Server port (default: 8000) | No       |

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── models.py          # Pydantic models
│   ├── routes.py          # API endpoints
│   └── search_service.py  # Vector search logic
├── main.py                # FastAPI application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── .dockerignore         # Docker ignore rules
```

## Technologies

- **FastAPI**: Modern web framework
- **OpenAI**: Embedding generation
- **Pinecone**: Vector database
- **Datasets**: Hugging Face datasets library
- **NumPy**: Numerical operations
- **Pydantic**: Data validation

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Type Checking

```bash
mypy .
```

## License

MIT License - DevFest Abeokuta 2025
