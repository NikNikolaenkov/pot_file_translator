import pytest
from src.config import Config
import os

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o")

def test_config_defaults(mock_env):
    config = Config()
    assert config.DEFAULT_MODEL == "gpt-4o"
    assert config.UPLOAD_FOLDER == "uploads"
    assert config.DOWNLOAD_FOLDER == "downloads"
    assert config.MAX_RETRIES == 5
    assert config.WAIT_TIME == 10
    assert config.BATCH_SIZE == 10 