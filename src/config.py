import os
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration settings for the POT translator service."""
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    UPLOAD_FOLDER: str = "uploads"
    DOWNLOAD_FOLDER: str = "downloads"
    MAX_RETRIES: int = 5
    WAIT_TIME: int = 10
    BATCH_SIZE: int = 10 