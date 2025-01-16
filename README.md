# POT File Translator OpenAI's

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

# Run application
flask run
```

### 2. Docker Installation

```bash
# Clone and setup
git clone [repository-url]
cd pot-translator
cp .env.example .env
# Edit .env with your settings

# Run with Docker Compose
docker-compose up --build
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
| file | file | POT file to translate |
| model | string | (Optional) OpenAI model name (default: gpt-4o) |

#### Example Requests:

1. Using curl:
```bash
curl -X POST http://localhost:5000/translate \
     -F "api_key=your-api-key" \
     -F "target_language=uk" \
     -F "file=@path/to/your/main.pot"
```

2. Using Python requests:
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

3. Using JavaScript/Fetch:
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
# Build and run with docker-compose
docker-compose up --build

# Stop services
docker-compose down

# Build image separately
docker build -t pot-translator .

# Run container separately
docker run -p 5000:5000 -e OPENAI_API_KEY=your-api-key pot-translator
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

3. Docker Issues:
   ```
   Error: Port 5000 already in use
   Solution: Change port in docker-compose.yml
   ```

## License

MIT License

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request