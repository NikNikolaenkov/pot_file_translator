import pytest
from src.config import Config
import os

def test_config_defaults():
    """Test configuration defaults without environment variables"""
    config = Config()
    assert config.UPLOAD_FOLDER == "uploads"
    assert config.DOWNLOAD_FOLDER == "downloads"
    assert config.MAX_RETRIES == 5
    assert config.WAIT_TIME == 10
    assert config.BATCH_SIZE == 10

def test_config_with_env_vars(monkeypatch):
    """Test configuration with environment variables"""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o")
    
    config = Config()
    assert config.OPENAI_API_KEY == "test-key"
    assert config.DEFAULT_MODEL == "gpt-4o" 