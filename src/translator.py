import os
import time
import polib
import logging
from openai import OpenAI
from typing import List, Tuple
from .config import Config

class PotTranslator:
    """POT file translator using OpenAI API."""

    def __init__(self, api_key: str, model: str = Config.DEFAULT_MODEL):
        """Initialize translator with API key and model."""
        try:
            self.client = OpenAI(api_key=api_key)
            self.model = model
            self.setup_logging()
        except Exception as e:
            logging.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise

    def setup_logging(self):
        """Configure logging."""
        logging.basicConfig(
            filename="translation.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def translate_batch(self, texts: List[str], target_language: str) -> List[str]:
        """Translate a batch of texts."""
        if not texts:
            return []

        for attempt in range(Config.MAX_RETRIES):
            try:
                joined_text = " ||| ".join(texts)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"Translate to {target_language}. Each sentence is separated by '|||'."},
                        {"role": "user", "content": joined_text}
                    ]
                )
                
                if not response.choices or not response.choices[0].message:
                    raise ValueError("Invalid response format")
                    
                translated_batch = response.choices[0].message.content.strip().split(" ||| ")
                
                if len(translated_batch) != len(texts):
                    raise ValueError("Mismatch between input and output batch size")
                
                return translated_batch
            except Exception as e:
                logging.error(f"Translation error: {str(e)}")
                if attempt == Config.MAX_RETRIES - 1:
                    return texts
                time.sleep(Config.WAIT_TIME)
        
        return texts

    def translate_pot_file(self, input_file: str, target_language: str) -> Tuple[bytes, str]:
        """Translate a POT file to the target language and return content and filename."""
        try:
            pot = polib.pofile(input_file)
            
            batch = []
            batch_entries = []
            
            for entry in pot:
                if not entry.msgstr:
                    batch.append(entry.msgid)
                    batch_entries.append(entry)
                    
                    if len(batch) >= Config.BATCH_SIZE:
                        translations = self.translate_batch(batch, target_language)
                        for entry, translation in zip(batch_entries, translations):
                            entry.msgstr = translation
                        batch.clear()
                        batch_entries.clear()
            
            if batch:
                translations = self.translate_batch(batch, target_language)
                for entry, translation in zip(batch_entries, translations):
                    entry.msgstr = translation
            
            # Створюємо тимчасовий файл для збереження
            output_file = os.path.join(Config.DOWNLOAD_FOLDER, f"{target_language}.po")
            os.makedirs(Config.DOWNLOAD_FOLDER, exist_ok=True)
            pot.save(output_file)
            
            # Читаємо вміст файлу
            with open(output_file, 'rb') as f:
                content = f.read()
            
            # Видаляємо тимчасовий файл
            try:
                os.remove(output_file)
            except:
                pass
                
            return content, f"{target_language}.po"
            
        except Exception as e:
            logging.error(f"Failed to translate POT file: {str(e)}")
            raise 