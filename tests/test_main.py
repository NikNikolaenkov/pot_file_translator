import pytest
from src.main import app
import io
from unittest.mock import patch
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_translate_no_api_key(client):
    response = client.post('/translate')
    assert response.status_code == 400
    assert b"API key is required" in response.data

def test_translate_no_file(client):
    data = {'api_key': 'test-key', 'target_language': 'uk'}
    response = client.post('/translate', data=data)
    assert response.status_code == 400
    assert b"No file provided" in response.data

def test_translate_success(client, tmp_path):
    with patch('src.main.PotTranslator') as MockTranslator:
        # Setup mock
        mock_instance = MockTranslator.return_value
        output_file = str(tmp_path / "uk.po")
        mock_instance.translate_pot_file.return_value = output_file
        
        # Create test file
        with open(output_file, 'w') as f:
            f.write('test content')
        
        # Make request
        data = {
            'api_key': 'test-key',
            'target_language': 'uk',
            'file': (io.BytesIO(b"test content"), 'test.pot')
        }
        
        response = client.post('/translate', data=data)
        
        assert response.status_code == 200
        MockTranslator.assert_called_once()
        mock_instance.translate_pot_file.assert_called_once() 