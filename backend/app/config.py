# Configuration module for FastAPI backend
import os
from functools import lru_cache
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())


class Settings:
    """
    Application settings loaded from environment variables.
    Manages API keys and configuration for OpenAI and Pinecone.
    """

    def __init__(self) -> None:
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.embedding_model = "text-embedding-3-large"
        self.index_name = "embedding-search"
        self.embedding_dimension = 3072  # For text-embedding-3-large
        self.pinecone_cloud = "aws"
        self.pinecone_region = "us-east-1"

    def validate_keys(self) -> bool:
        """Check if required API keys are present"""
        if not self.pinecone_api_key or not self.openai_api_key:
            return False
        return True

    def get_config_info(self) -> dict:
        """Return configuration information (without exposing full API keys)"""
        return {
            "pinecone_configured": bool(self.pinecone_api_key),
            "openai_configured": bool(self.openai_api_key),
            "embedding_model": self.embedding_model,
            "embedding_dimension": self.embedding_dimension,
            "default_index_name": self.index_name,
        }


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache ensures we only create one Settings instance.
    """
    return Settings()
