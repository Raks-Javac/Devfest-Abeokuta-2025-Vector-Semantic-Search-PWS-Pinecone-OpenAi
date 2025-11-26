# Core logic for vector search operations
import openai
from pinecone import Pinecone, ServerlessSpec
from datasets import load_dataset
from numpy import dot, array
from numpy.linalg import norm
from typing import List, Dict, Any, Optional, Tuple
from tqdm import tqdm
import time

from .config import get_settings


class VectorSearchService:
    """
    Service class handling:
    - Text embedding generation using OpenAI
    - Vector indexing with Pinecone
    - Similarity search queries
    - Dataset loading and indexing
    """

    def __init__(self):
        self.settings = get_settings()

        # Validate API keys
        if not self.settings.validate_keys():
            raise ValueError("Missing required API keys. Check your .env file.")

        # Initialize OpenAI client
        openai.api_key = self.settings.openai_api_key

        # Initialize Pinecone client
        self.pc = Pinecone(api_key=self.settings.pinecone_api_key)

        # Cache for loaded dataset
        self._dataset_cache = None
        self._contexts_cache = None

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate vector embeddings from text using OpenAI API.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        response = openai.embeddings.create(
            input=texts, model=self.settings.embedding_model
        )

        embeddings = [r.embedding for r in response.data]
        return embeddings

    def calculate_similarity(self, text1: str, text2: str) -> Tuple[float, float]:
        """
        Calculate dot product and cosine similarity between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Tuple of (dot_product, cosine_similarity)
        """
        embeddings = self.create_embeddings([text1, text2])
        a = array(embeddings[0])
        b = array(embeddings[1])

        # Dot product
        dot_product = float(dot(a, b))

        # Cosine similarity
        cos_sim = float(dot(a, b) / (norm(a) * norm(b)))

        return dot_product, cos_sim

    def list_indexes(self) -> List[str]:
        """
        Get list of all Pinecone indexes.

        Returns:
            List of index names
        """
        indexes = self.pc.list_indexes()
        return [index.name for index in indexes]

    def create_index(
        self,
        index_name: Optional[str] = None,
        dimension: int = 3072,
        metric: str = "cosine",
        cloud: str = "aws",
        region: str = "us-east-1",
    ) -> Dict[str, Any]:
        """
        Create a new Pinecone vector index.

        Args:
            index_name: Name of the index (uses default if None)
            dimension: Vector dimension
            metric: Distance metric (cosine, euclidean, dotproduct)
            cloud: Cloud provider
            region: Cloud region

        Returns:
            Dictionary with creation status and details
        """
        if index_name is None:
            index_name = self.settings.index_name

        # Check if index already exists
        existing_indexes = self.list_indexes()
        if index_name in existing_indexes:
            return {
                "success": False,
                "message": f"Index '{index_name}' already exists",
                "index_name": index_name,
            }

        # Create the index
        self.pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(cloud=cloud, region=region),
        )

        # Wait for index to be ready
        while not self.pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

        return {
            "success": True,
            "message": f"Index '{index_name}' created successfully",
            "index_name": index_name,
            "dimension": dimension,
            "metric": metric,
        }

    def get_index_stats(self, index_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics for a Pinecone index.

        Args:
            index_name: Name of the index (uses default if None)

        Returns:
            Dictionary with index statistics
        """
        if index_name is None:
            index_name = self.settings.index_name

        index = self.pc.Index(index_name)
        stats = index.describe_index_stats()

        return {
            "index_name": index_name,
            "dimension": stats.dimension,
            "total_vector_count": stats.total_vector_count,
            "namespaces": stats.namespaces,
        }

    def load_dataset(
        self,
        dataset_name: str = "squad_v2",
        split: str = "train",
        preview_count: int = 5,
    ) -> Dict[str, Any]:
        """
        Load dataset from Hugging Face.

        Args:
            dataset_name: Name of the dataset
            split: Dataset split to load
            preview_count: Number of samples to preview

        Returns:
            Dictionary with dataset information and preview
        """
        # Load dataset
        dataset = load_dataset(dataset_name, split=split)

        # Extract unique contexts
        contexts = list(set(dataset["context"]))

        # Cache for later use
        self._dataset_cache = dataset
        self._contexts_cache = contexts

        # Create preview
        preview = []
        for i in range(min(preview_count, len(dataset))):
            preview.append(
                {
                    "id": dataset[i].get("id", f"sample_{i}"),
                    "title": dataset[i].get("title", "N/A"),
                    "context": (
                        dataset[i]["context"][:200] + "..."
                        if len(dataset[i]["context"]) > 200
                        else dataset[i]["context"]
                    ),
                    "question": dataset[i].get("question", "N/A"),
                }
            )

        return {
            "dataset_name": dataset_name,
            "split": split,
            "total_samples": len(dataset),
            "unique_contexts": len(contexts),
            "preview": preview,
        }

    def index_dataset(
        self,
        index_name: Optional[str] = None,
        batch_size: int = 100,
        max_contexts: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Index dataset contexts into Pinecone.

        Args:
            index_name: Name of the index (uses default if None)
            batch_size: Batch size for processing
            max_contexts: Maximum number of contexts to index (None for all)

        Returns:
            Dictionary with indexing results
        """
        if index_name is None:
            index_name = self.settings.index_name

        # Ensure dataset is loaded
        if self._contexts_cache is None:
            self.load_dataset()

        contexts = self._contexts_cache

        # Limit contexts if specified
        if max_contexts is not None:
            contexts = contexts[:max_contexts]

        # Get index
        index = self.pc.Index(index_name)

        # Process in batches
        indexed_count = 0
        for i in tqdm(range(0, len(contexts), batch_size), desc="Indexing batches"):
            i_end = min(i + batch_size, len(contexts))

            context_batch = contexts[i:i_end]
            id_batch = [str(x) for x in range(i, i_end)]

            # Create embeddings
            embeds = self.create_embeddings(context_batch)

            # Create metadata
            metadata = [{"context": x} for x in context_batch]

            # Prepare vectors for upsert
            to_upsert = list(zip(id_batch, embeds, metadata))

            # Upsert to index
            index.upsert(vectors=to_upsert)

            indexed_count += len(context_batch)

        # Get final stats
        stats = self.get_index_stats(index_name)

        return {
            "success": True,
            "message": f"Successfully indexed {indexed_count} contexts",
            "indexed_count": indexed_count,
            "index_name": index_name,
            "stats": stats,
        }

    def semantic_search(
        self, query: str, top_k: int = 3, index_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search on the vector database.

        Args:
            query: Search query text
            top_k: Number of results to return
            index_name: Name of the index (uses default if None)

        Returns:
            List of search matches with scores and contexts
        """
        if index_name is None:
            index_name = self.settings.index_name

        # Create query embedding
        query_embedding = self.create_embeddings([query])[0]

        # Get index and search
        index = self.pc.Index(index_name)
        results = index.query(
            vector=query_embedding, top_k=top_k, include_metadata=True
        )

        # Format results
        matches = []
        for match in results.matches:
            matches.append(
                {
                    "id": match.id,
                    "score": float(match.score),
                    "context": match.metadata.get("context", ""),
                }
            )

        return matches
