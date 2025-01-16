import pytest
import os

@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch, tmp_path):
    """Setup test environment"""
    # Set environment variables
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o")
    
    # Create necessary directories
    uploads = tmp_path / "uploads"
    downloads = tmp_path / "downloads"
    uploads.mkdir()
    downloads.mkdir()
    
    # Set temporary directories in environment
    monkeypatch.setenv("UPLOAD_FOLDER", str(uploads))
    monkeypatch.setenv("DOWNLOAD_FOLDER", str(downloads))
    
    yield 