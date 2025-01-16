import pytest
from src.main import app
import io
from unittest.mock import patch
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_env():
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test-key',
        'OPENAI_MODEL': 'gpt-4o'
    }):
        yield

def test_translate_no_api_key(client):
    response = client.post('/translate')
    assert response.status_code == 400
    assert b"API key is required" in response.data

def test_translate_no_file(client):
    data = {'api_key': 'test-key', 'target_language': 'uk'}
    response = client.post('/translate', data=data)
    assert response.status_code == 400
    assert b"No file provided" in response.data

def test_translate_success(client, tmp_path, mock_env):
    with patch('src.main.PotTranslator') as MockTranslator:
        mock_instance = MockTranslator.return_value
        mock_instance.translate_pot_file.return_value = str(tmp_path / "uk.po")
        
        data = {
            'api_key': 'test-key',
            'target_language': 'uk',
            'file': (io.BytesIO(b"test content"), 'test.pot')
        }
        
        with patch('os.path.exists', return_value=True):
            response = client.post('/translate', data=data)
        
        assert response.status_code == 200
        MockTranslator.assert_called_once_with(api_key='test-key', model='gpt-4o') 