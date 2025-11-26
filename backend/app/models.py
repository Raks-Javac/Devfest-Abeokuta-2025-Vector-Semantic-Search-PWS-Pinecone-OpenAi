# Pydantic models for request/response validation
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# Embedding Models
class EmbeddingRequest(BaseModel):
    """Request model for creating embeddings"""

    texts: List[str] = Field(..., description="List of texts to embed", min_length=1)

    class Config:
        json_schema_extra = {
            "example": {"texts": ["Hello world", "Vector search is powerful"]}
        }


class EmbeddingResponse(BaseModel):
    """Response model for embedding creation"""

    embeddings: List[List[float]] = Field(..., description="Generated embeddings")
    model: str = Field(..., description="Model used for embedding")
    dimension: int = Field(..., description="Dimension of each embedding")
    count: int = Field(..., description="Number of embeddings generated")


class SimilarityRequest(BaseModel):
    """Request model for calculating similarity between texts"""

    text1: str = Field(..., description="First text")
    text2: str = Field(..., description="Second text")


class SimilarityResponse(BaseModel):
    """Response model for similarity calculation"""

    dot_product: float = Field(..., description="Dot product similarity")
    cosine_similarity: float = Field(..., description="Cosine similarity score")
    text1: str
    text2: str


# Index Models
class IndexCreateRequest(BaseModel):
    """Request model for creating a vector index"""

    index_name: Optional[str] = Field(None, description="Name of the index to create")
    dimension: Optional[int] = Field(3072, description="Dimension of vectors")
    metric: Optional[str] = Field(
        "cosine", description="Distance metric (cosine, euclidean, dotproduct)"
    )
    cloud: Optional[str] = Field("aws", description="Cloud provider")
    region: Optional[str] = Field("us-east-1", description="Cloud region")


class IndexResponse(BaseModel):
    """Response model for index operations"""

    success: bool
    message: str
    index_name: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class IndexStatsResponse(BaseModel):
    """Response model for index statistics"""

    index_name: str
    dimension: int
    total_vector_count: int
    namespaces: Dict[str, Any]


# Search Models
class SearchRequest(BaseModel):
    """Request model for semantic search"""

    query: str = Field(..., description="Search query text")
    top_k: int = Field(3, description="Number of results to return", ge=1, le=100)
    index_name: Optional[str] = Field(None, description="Index to search in")

    class Config:
        json_schema_extra = {"example": {"query": "What is a beehive?", "top_k": 3}}


class SearchMatch(BaseModel):
    """Single search result match"""

    score: float = Field(..., description="Similarity score")
    context: str = Field(..., description="Matched context text")
    id: Optional[str] = Field(None, description="Vector ID")


class SearchResponse(BaseModel):
    """Response model for search results"""

    query: str
    matches: List[SearchMatch]
    count: int


# Dataset Models
class DatasetLoadRequest(BaseModel):
    """Request model for loading dataset"""

    dataset_name: str = Field("squad_v2", description="Hugging Face dataset name")
    split: str = Field("train", description="Dataset split to load")
    preview_count: int = Field(
        5, description="Number of samples to preview", ge=1, le=100
    )


class DatasetLoadResponse(BaseModel):
    """Response model for dataset loading"""

    dataset_name: str
    split: str
    total_samples: int
    unique_contexts: int
    preview: List[Dict[str, Any]]


class DatasetIndexRequest(BaseModel):
    """Request model for indexing dataset"""

    index_name: Optional[str] = Field(None, description="Index to use")
    batch_size: int = Field(100, description="Batch size for indexing", ge=1, le=500)
    max_contexts: Optional[int] = Field(
        None, description="Maximum contexts to index (None for all)"
    )


class DatasetIndexResponse(BaseModel):
    """Response model for dataset indexing"""

    success: bool
    message: str
    indexed_count: int
    index_name: str
    stats: Optional[Dict[str, Any]] = None


# Health and Config Models
class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    api_keys_configured: bool
    embedding_model: str


class ConfigResponse(BaseModel):
    """Configuration information response"""

    pinecone_configured: bool
    openai_configured: bool
    embedding_model: str
    embedding_dimension: int
    default_index_name: str
