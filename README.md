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

Clone repository
git clone [repository-url]
cd pot-translator
Create virtual environment
python -m venv venv
Activate virtual environment
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
Install dependencies
pip install -r requirements.txt
Setup environment
cp .env.example .env
Edit .env with your settings
Run application
flask run

### 2. Docker Installation

1. Clone the repository
2. Build Docker image
docker build -t pot-translator .
3. Run Docker container
docker run -p 5000:5000 pot-translator

Clone and setup
git clone [repository-url]
cd pot-translator
cp .env.example .env
Edit .env with your settings
Run with Docker
docker-compose up --build

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
     -F "model=gpt-4o" \
     -F "file=@path/to/your/main.pot"
```

2. Using Python requests:
```python
import requests

# API endpoint
url = 'http://localhost:5000/translate'

# Prepare files and data
files = {
    'file': ('main.pot', open('path/to/your/main.pot', 'rb'), 'application/x-gettext')
}
data = {
    'api_key': 'your-api-key',
    'target_language': 'uk',
    'model': 'gpt-4o'  # optional
}

# Send request
response = requests.post(url, files=files, data=data)

# Handle response
if response.status_code == 200:
    # Save translated file
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
formData.append('model', 'gpt-4');  // optional

fetch('http://localhost:5000/translate', {
    method: 'POST',
    body: formData
})
.then(response => {
    if (response.ok) return response.blob();
    return response.json().then(err => Promise.reject(err));
})
.then(blob => {
    // Handle successful response
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
| OPENAI_MODEL | OpenAI model to use | gpt-4 |
| FLASK_ENV | Environment mode | development |
| FLASK_DEBUG | Debug mode | 1 |
| MAX_RETRIES | Max translation retries | 5 |
| WAIT_TIME | Retry wait time (seconds) | 10 |
| BATCH_SIZE | Translation batch size | 10 |

## File Structure
```
pot-translator/
├── src/
│   ├── main.py        # REST API implementation
│   ├── translator.py   # Translation logic
│   └── config.py      # Configuration settings
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose config
├── requirements.txt   # Python dependencies
└── .env.example      # Environment template
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

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Docker Commands
```bash
# Build image
docker build -t pot-translator .

# Run container
docker run -p 5000:5000 -e OPENAI_API_KEY=your-api-key pot-translator

# Stop services
docker-compose down
```

## License

MIT License

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request