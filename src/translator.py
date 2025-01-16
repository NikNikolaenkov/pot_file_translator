import os
import time
import polib
import logging
from openai import OpenAI
from typing import List, Optional
from .config import Config

class PotTranslator:
    def __init__(self, api_key: str, model: str = Config.DEFAULT_MODEL):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename="translation.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def translate_batch(self, texts: List[str], target_language: str) -> List[str]:
        for attempt in range(Config.MAX_RETRIES):
            try:
                joined_text = " ||| ".join(texts)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are a professional translator. Translate the following text into {target_language}. Each sentence is separated by '|||'. Preserve the order."},
                        {"role": "user", "content": f"Translate the following:\n\n{joined_text}"}
                    ]
                )
                translated_batch = response.choices[0].message.content.strip().split(" ||| ")
                
                if len(translated_batch) != len(texts):
                    raise ValueError("Mismatch between input and output batch size")
                
                return translated_batch
            except Exception as e:
                logging.error(f"Translation error: {str(e)}")
                if attempt == Config.MAX_RETRIES - 1:
                    return texts
                time.sleep(Config.WAIT_TIME)

    def translate_pot_file(self, input_file: str, target_language: str) -> str:
        pot = polib.pofile(input_file)
        output_file = os.path.join(Config.DOWNLOAD_FOLDER, f"{target_language}.po")
        
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
        
        os.makedirs(Config.DOWNLOAD_FOLDER, exist_ok=True)
        pot.save(output_file)
        return output_file 