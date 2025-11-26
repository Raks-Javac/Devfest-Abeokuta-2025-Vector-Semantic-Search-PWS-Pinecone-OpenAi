# API Routes for Vector Search endpoints
from fastapi import APIRouter, HTTPException, status
from typing import List

from .models import (
    EmbeddingRequest,
    EmbeddingResponse,
    SimilarityRequest,
    SimilarityResponse,
    IndexCreateRequest,
    IndexResponse,
    IndexStatsResponse,
    SearchRequest,
    SearchResponse,
    SearchMatch,
    DatasetLoadRequest,
    DatasetLoadResponse,
    DatasetIndexRequest,
    DatasetIndexResponse,
    HealthResponse,
    ConfigResponse,
)
from .search_service import VectorSearchService
from .config import get_settings

# Create router
router = APIRouter()


# Initialize service (will be created once per request)
def get_service():
    """Dependency to get vector search service"""
    try:
        return VectorSearchService()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Health and Config Endpoints
@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health and configuration status"""
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        api_keys_configured=settings.validate_keys(),
        embedding_model=settings.embedding_model,
    )


@router.get("/config", response_model=ConfigResponse, tags=["Health"])
async def get_config():
    """Get configuration information"""
    settings = get_settings()
    return ConfigResponse(**settings.get_config_info())


# Embedding Endpoints
@router.post(
    "/api/embeddings/create", response_model=EmbeddingResponse, tags=["Embeddings"]
)
async def create_embeddings(request: EmbeddingRequest):
    """
    Generate embeddings from text using OpenAI.

    - **texts**: List of text strings to embed
    """
    try:
        service = get_service()
        embeddings = service.create_embeddings(request.texts)

        return EmbeddingResponse(
            embeddings=embeddings,
            model=service.settings.embedding_model,
            dimension=len(embeddings[0]) if embeddings else 0,
            count=len(embeddings),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create embeddings: {str(e)}",
        )


@router.post(
    "/api/embeddings/similarity", response_model=SimilarityResponse, tags=["Embeddings"]
)
async def calculate_similarity(request: SimilarityRequest):
    """
    Calculate similarity between two texts.

    - **text1**: First text
    - **text2**: Second text

    Returns both dot product and cosine similarity.
    """
    try:
        service = get_service()
        dot_product, cosine_sim = service.calculate_similarity(
            request.text1, request.text2
        )

        return SimilarityResponse(
            dot_product=dot_product,
            cosine_similarity=cosine_sim,
            text1=request.text1,
            text2=request.text2,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate similarity: {str(e)}",
        )


# Index Management Endpoints
@router.get("/api/indexes/list", response_model=List[str], tags=["Index Management"])
async def list_indexes():
    """List all available Pinecone indexes"""
    try:
        service = get_service()
        indexes = service.list_indexes()
        return indexes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list indexes: {str(e)}",
        )


@router.post(
    "/api/indexes/create", response_model=IndexResponse, tags=["Index Management"]
)
async def create_index(request: IndexCreateRequest):
    """
    Create a new Pinecone vector index.

    - **index_name**: Name of the index (optional, uses default if not provided)
    - **dimension**: Vector dimension (default: 3072 for text-embedding-3-large)
    - **metric**: Distance metric (cosine, euclidean, dotproduct)
    - **cloud**: Cloud provider (default: aws)
    - **region**: Cloud region (default: us-east-1)
    """
    try:
        service = get_service()
        result = service.create_index(
            index_name=request.index_name,
            dimension=request.dimension,
            metric=request.metric,
            cloud=request.cloud,
            region=request.region,
        )

        return IndexResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create index: {str(e)}",
        )


@router.get(
    "/api/indexes/{index_name}/stats",
    response_model=IndexStatsResponse,
    tags=["Index Management"],
)
async def get_index_stats(index_name: str):
    """
    Get statistics for a specific index.

    - **index_name**: Name of the index
    """
    try:
        service = get_service()
        stats = service.get_index_stats(index_name)
        return IndexStatsResponse(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=(
                status.HTTP_404_NOT_FOUND
                if "not found" in str(e).lower()
                else status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=f"Failed to get index stats: {str(e)}",
        )


# Dataset Endpoints
@router.post("/api/dataset/load", response_model=DatasetLoadResponse, tags=["Dataset"])
async def load_dataset(request: DatasetLoadRequest):
    """
    Load a dataset from Hugging Face.

    - **dataset_name**: Name of the dataset (default: squad_v2)
    - **split**: Dataset split to load (default: train)
    - **preview_count**: Number of samples to preview (default: 5)
    """
    try:
        service = get_service()
        result = service.load_dataset(
            dataset_name=request.dataset_name,
            split=request.split,
            preview_count=request.preview_count,
        )

        return DatasetLoadResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load dataset: {str(e)}",
        )


@router.post(
    "/api/dataset/index", response_model=DatasetIndexResponse, tags=["Dataset"]
)
async def index_dataset(request: DatasetIndexRequest):
    """
    Index dataset contexts into Pinecone.

    - **index_name**: Name of the index (optional, uses default if not provided)
    - **batch_size**: Batch size for processing (default: 100)
    - **max_contexts**: Maximum number of contexts to index (optional, indexes all if not provided)

    Note: This operation may take a while depending on dataset size.
    """
    try:
        service = get_service()
        result = service.index_dataset(
            index_name=request.index_name,
            batch_size=request.batch_size,
            max_contexts=request.max_contexts,
        )

        return DatasetIndexResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to index dataset: {str(e)}",
        )


# Search Endpoints
@router.post("/api/search", response_model=SearchResponse, tags=["Search"])
async def semantic_search(request: SearchRequest):
    """
    Perform semantic search on the vector database.

    - **query**: Search query text
    - **top_k**: Number of results to return (default: 3, max: 100)
    - **index_name**: Index to search in (optional, uses default if not provided)
    """
    try:
        service = get_service()
        matches = service.semantic_search(
            query=request.query, top_k=request.top_k, index_name=request.index_name
        )

        # Convert to SearchMatch models
        search_matches = [
            SearchMatch(
                score=match["score"], context=match["context"], id=match.get("id")
            )
            for match in matches
        ]

        return SearchResponse(
            query=request.query, matches=search_matches, count=len(search_matches)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to perform search: {str(e)}",
        )
