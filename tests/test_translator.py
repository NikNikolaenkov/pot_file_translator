import pytest
from unittest.mock import Mock, patch
from src.translator import PotTranslator
from src.config import Config
import os

class TestPotTranslator:
    @pytest.fixture
    def mock_openai_client(self, mocker):
        mock_response = Mock()
        mock_response.choices = [
            Mock(message=Mock(content="Привіт ||| Світ"))
        ]
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        
        # Створюємо мок для конструктора OpenAI
        mock_openai = mocker.patch('openai.OpenAI')
        mock_openai.return_value = mock_client
        return mock_client

    @pytest.fixture
    def translator(self):
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'OPENAI_MODEL': 'gpt-4o'
        }):
            return PotTranslator(api_key="test-key")

    @pytest.fixture
    def sample_pot_file(self, tmp_path):
        content = '''msgid ""
msgstr ""
"Project-Id-Version: Test\\n"
"Content-Type: text/plain; charset=UTF-8\\n"

msgid "Hello"
msgstr ""

msgid "World"
msgstr ""
'''
        pot_file = tmp_path / "test.pot"
        pot_file.write_text(content)
        return str(pot_file)

    def test_translate_batch(self, translator, mock_openai_client):
        texts = ["Hello", "World"]
        result = translator.translate_batch(texts, "uk")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result == ["Привіт", "Світ"]

    def test_translate_pot_file(self, translator, sample_pot_file, mock_openai_client, tmp_path):
        with patch('os.makedirs'):
            target_language = "uk"
            output_file = translator.translate_pot_file(sample_pot_file, target_language)
            assert output_file.endswith(f"{target_language}.po") 