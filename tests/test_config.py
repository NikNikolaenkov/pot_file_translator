from src.config import Config

def test_config_defaults():
    config = Config()
    assert config.DEFAULT_MODEL == "gpt-4o"
    assert config.UPLOAD_FOLDER == "uploads"
    assert config.DOWNLOAD_FOLDER == "downloads"
    assert config.MAX_RETRIES == 5
    assert config.WAIT_TIME == 10
    assert config.BATCH_SIZE == 10 