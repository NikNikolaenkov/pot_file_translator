import pytest
import os

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Автоматично встановлює змінні середовища для тестів"""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o") 