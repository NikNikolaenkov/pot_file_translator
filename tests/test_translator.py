import pytest
from unittest.mock import Mock, patch
from src.translator import PotTranslator
from src.config import Config
import os
import polib

class TestPotTranslator:
    @pytest.fixture
    def mock_openai(self, mocker):
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Привіт ||| Світ"))]
        mock_client.chat.completions.create.return_value = mock_response
        mocker.patch('openai.OpenAI', return_value=mock_client)
        return mock_client

    @pytest.fixture
    def translator(self, mock_openai):
        return PotTranslator(api_key="test-key")

    @pytest.fixture
    def sample_pot_content(self):
        return '''
msgid ""
msgstr ""
"Project-Id-Version: Test Project\\n"
"POT-Creation-Date: 2024-03-21\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "Hello World"
msgstr ""

msgid "Welcome"
msgstr ""
'''

    @pytest.fixture
    def sample_pot_file(self, sample_pot_content, tmp_path):
        pot_file = tmp_path / "test.pot"
        pot_file.write_text(sample_pot_content)
        return str(pot_file)

    def test_init(self, translator):
        assert translator.model == Config.DEFAULT_MODEL
        assert translator.client is not None

    def test_translate_batch(self, translator):
        texts = ["Hello", "World"]
        result = translator.translate_batch(texts, "uk")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result == ["Привіт", "Світ"]

    @patch('os.makedirs')
    def test_translate_pot_file(self, mock_makedirs, translator, sample_pot_file):
        target_language = "uk"
        output_file = translator.translate_pot_file(sample_pot_file, target_language)
        
        assert output_file.endswith(f"{target_language}.po")
        mock_makedirs.assert_called_once_with(Config.DOWNLOAD_FOLDER, exist_ok=True) 