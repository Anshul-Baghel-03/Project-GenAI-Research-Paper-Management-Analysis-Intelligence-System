"""
Configuration Module - Centralized Settings Management
=======================================================
DAY 1: This module handles all configuration and environment variables.

SOLID Principle: Single Responsibility Principle (SRP)
- This class has ONE job: manage configuration settings

Topics to teach:
- Environment variables and security
- Pydantic-style configuration
- Singleton pattern for settings
"""

import os 
from dotenv import load_dotenv
from dataclasses import dataclass

# Fix tokenizers parallelism warning (must be set before importing transformers)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load environment variables from .env file
load_dotenv()

@dataclass
class Settings:
    """
    Centralized configuration settings for the RAG application.
    

    GROQ_API_KEY:str =os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY:str =os.getenv("TAVILY_API_KEY")
    LLM_MODEL:str =os.getenv("LLM_MODEL")
    LLM_TEMPERATURE:float =os.getenv("LLM_TEMPERATURE")
    EMBEDDING_MODEL:str =os.getenv("EMBEDDING_MODEL")
    CHUNK_SIZE:int =os.getenv("CHUNK_SIZE")
    CHUNK_OVERLAP:int=os.getenv("CHUNK_OVERLAP")
    FAST_INDEX_PATH:str=os.getenv("FAST_INDEX_PATH")
    TOP_K_RESULT:str=os.getenv("TOP_K_RESULT")
    All API keys and configuration values are loaded from environment variables
    for security. Never hardcode API keys in your code!
    """


    # API Keys (loaded from environment)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    
    # LLM Configuration
    LLM_MODEL: str = "llama-3.1-8b-instant"  # Free Groq model
    LLM_TEMPERATURE: float = 0.7
    
    # Embedding Configuration  
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"  # Free HuggingFace model
    
    # Document Processing Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Vector Store Configuration
    FAISS_INDEX_PATH: str = "data/faiss_index"
    
    # Retrieval Configuration
    TOP_K_RESULTS: int = 3
    
    
    def validate(self)->bool:
        """Check if required API key are set"""
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set. Please add it to your .env file.")
        if not self.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is not set. Please add it to your .env file.")
        return True


# Create a singleton instance
settings = Settings()