# FastAPI entrypoint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router
from app.config import get_settings

# Initialize settings
settings = get_settings()

# Create FastAPI app with metadata
app = FastAPI(
    title="Vector Search API",
    description="API for semantic search using OpenAI embeddings and Pinecone vector database",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


# @app.get("/")
# async def root():
#     """Root endpoint with API information"""
#     return {
#         "message": "Vector Search API is running",
#         "version": "1.0.0",
#         "docs": "/docs",
#         "health": "/health",
#     }
