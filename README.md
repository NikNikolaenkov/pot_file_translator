# POT File Translator

A service for automatic translation of POT localization files using OpenAI GPT. This service helps translate localization files (.pot) into different languages using OpenAI's powerful language models.

## Author
Nikolaenkov (NikNikolaenkov@gmail.com)

## Features

- 🚀 Batch translation for API optimization
- 💾 Support for existing translations
- 📝 Detailed translation logging
- 🔄 Automatic error handling and retries
- 🔧 Multiple OpenAI model support
- 📊 Progress tracking and saving
- 🐳 Docker support
- 🌐 Support for remote file loading via URL
- ⚙️ Configurable port settings

## Installation

### 1. Local Installation

```bash
# Clone repository
git clone [repository-url]
cd pot-translator

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Run application (default port 5000)
flask run

# Or run on custom port
FLASK_PORT=8080 flask run
```

### 2. Docker Installation

```bash
# Clone and setup
git clone [repository-url]
cd pot-translator
cp .env.example .env
# Edit .env with your settings

# Run with Docker Compose (default port 5000)
docker-compose up --build

# Or run on custom port
FLASK_PORT=8080 docker-compose up --build
```

## API Usage Guide

### Translating a POT File

The service provides a single endpoint for translation:

**Endpoint:** `POST /translate`

#### Required Parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| api_key | string | Your OpenAI API key |
| target_language | string | Two-letter language code (e.g., 'uk', 'es', 'de') |
| file | file | POT file to translate (mutually exclusive with file_url) |
| file_url | string | URL to POT file (mutually exclusive with file) |
| model | string | (Optional) OpenAI model name (default: gpt-4o) |

#### Example Requests:

1. Using curl with local file:
```bash
curl -X POST http://localhost:5000/translate \
     -F "api_key=your-api-key" \
     -F "target_language=uk" \
     -F "file=@path/to/your/main.pot"
```

2. Using curl with remote file:
```bash
curl -X POST http://localhost:5000/translate \
     -F "api_key=your-api-key" \
     -F "target_language=uk" \
     -F "file_url=https://example.com/path/to/main.pot"
```

3. Using Python requests with local file:
```python
import requests

url = 'http://localhost:5000/translate'

files = {
    'file': ('main.pot', open('path/to/your/main.pot', 'rb'), 'application/x-gettext')
}
data = {
    'api_key': 'your-api-key',
    'target_language': 'uk'
}

response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    with open('translated.po', 'wb') as f:
        f.write(response.content)
    print("Translation successful!")
else:
    print(f"Error: {response.json()['error']}")
```

4. Using Python requests with remote file:
```python
import requests

url = 'http://localhost:5000/translate'
data = {
    'api_key': 'your-api-key',
    'target_language': 'uk',
    'file_url': 'https://example.com/path/to/main.pot'
}

response = requests.post(url, data=data)

if response.status_code == 200:
    with open('translated.po', 'wb') as f:
        f.write(response.content)
    print("Translation successful!")
else:
    print(f"Error: {response.json()['error']}")
```

5. Using JavaScript/Fetch with local file:
```javascript
const formData = new FormData();
formData.append('file', potFile);  // potFile is your .pot file
formData.append('api_key', 'your-api-key');
formData.append('target_language', 'uk');

fetch('http://localhost:5000/translate', {
    method: 'POST',
    body: formData
})
.then(response => {
    if (response.ok) return response.blob();
    return response.json().then(err => Promise.reject(err));
})
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'translated.po';
    a.click();
})
.catch(error => console.error('Error:', error));
```

6. Using JavaScript/Fetch with remote file:
```javascript
const formData = new FormData();
formData.append('file_url', 'https://example.com/path/to/main.pot');
formData.append('api_key', 'your-api-key');
formData.append('target_language', 'uk');

fetch('http://localhost:5000/translate', {
    method: 'POST',
    body: formData
})
.then(response => {
    if (response.ok) return response.blob();
    return response.json().then(err => Promise.reject(err));
})
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'translated.po';
    a.click();
})
.catch(error => console.error('Error:', error));
```

#### Response:

Success (200):
- Content-Type: application/x-gettext
- Body: Translated PO file content

Error (400/500):
```json
{
    "error": "Error description"
}
```

## Configuration

### Environment Variables

Create `.env` file from template:
```bash
cp .env.example .env
```

Available settings:

| Variable | Description | Default |
|----------|-------------|---------|
| OPENAI_API_KEY | Your OpenAI API key | required |
| OPENAI_MODEL | OpenAI model to use | gpt-4o |
| FLASK_ENV | Environment mode | development |
| FLASK_DEBUG | Debug mode | 1 |
| FLASK_PORT | Server port | 5000 |
| MAX_RETRIES | Max translation retries | 5 |
| WAIT_TIME | Retry wait time (seconds) | 10 |
| BATCH_SIZE | Translation batch size | 10 |

## Project Structure
```
pot-translator/
├── src/
│   ├── __init__.py
│   ├── main.py        # REST API implementation
│   ├── translator.py   # Translation logic
│   └── config.py      # Configuration settings
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_main.py
│   └── test_translator.py
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose config
├── requirements.txt   # Python dependencies
└── .env.example      # Environment template
```

## Dependencies

Main dependencies (see requirements.txt for full list):
- Flask==2.3.3
- polib==1.2.0
- openai==1.59.7
- python-dotenv==1.0.0
- pytest==7.4.3
- requests==2.31.0

## Development

### Running Tests
```bash
# Run all tests with coverage
python -m pytest tests/ -v --cov=src

# Run specific test file
python -m pytest tests/test_translator.py -v
```

### Docker Commands
```bash
# Build and run with docker-compose (default port)
docker-compose up --build

# Run on custom port
FLASK_PORT=8080 docker-compose up --build

# Stop services
docker-compose down

# Build image separately
docker build -t pot-translator .

# Run container separately (default port)
docker run -p 5000:5000 -e OPENAI_API_KEY=your-api-key pot-translator

# Run container on custom port
docker run -p 8080:5000 -e OPENAI_API_KEY=your-api-key -e FLASK_PORT=8080 pot-translator
```

## Troubleshooting

### Common Issues and Solutions:

1. API Key Issues:
   ```
   Error: Invalid API key
   Solution: Check OPENAI_API_KEY in .env file
   ```

2. File Upload Issues:
   ```
   Error: Invalid file format
   Solution: Ensure file has .pot extension
   ```

3. URL Issues:
   ```
   Error: Failed to download file from URL
   Solution: Check if URL is accessible and points to a valid .pot file
   ```

4. Port Issues:
   ```
   Error: Port 5000 already in use
   Solution: Set different port in .env file or use FLASK_PORT environment variable
   ```

## License

MIT License

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request