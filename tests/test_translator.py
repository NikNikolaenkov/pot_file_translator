import pytest
from unittest.mock import Mock, patch
from src.translator import PotTranslator
from src.config import Config
import os

class TestPotTranslator:
    @pytest.fixture
    def mock_openai_client(self, mocker):
        # Створюємо мок для відповіді
        mock_response = Mock()
        mock_response.choices = [
            Mock(message=Mock(content="Привіт ||| Світ"))
        ]
        
        # Створюємо мок для chat.completions
        mock_completions = Mock()
        mock_completions.create.return_value = mock_response
        
        # Створюємо мок для chat
        mock_chat = Mock()
        mock_chat.completions = mock_completions
        
        # Створюємо мок для клієнта OpenAI
        mock_client = Mock()
        mock_client.chat = mock_chat
        
        # Патчимо конструктор OpenAI
        mocker.patch('openai.OpenAI', return_value=mock_client)
        
        return mock_client

    @pytest.fixture
    def translator(self):
        # Використовуємо patch для обходу ініціалізації реального клієнта
        with patch('openai.OpenAI') as mock_openai:
            instance = PotTranslator(api_key="test-key")
            # Переконуємося, що конструктор був викликаний з правильними параметрами
            mock_openai.assert_called_once_with(api_key="test-key")
            return instance

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
        
        # Перевіряємо, що API був викликаний правильно
        mock_openai_client.chat.completions.create.assert_called_once()

    def test_translate_pot_file(self, translator, sample_pot_file, mock_openai_client, tmp_path):
        with patch('os.makedirs'):
            target_language = "uk"
            output_file = translator.translate_pot_file(sample_pot_file, target_language)
            assert output_file.endswith(f"{target_language}.po")
            
            # Перевіряємо, що API був викликаний
            assert mock_openai_client.chat.completions.create.called 