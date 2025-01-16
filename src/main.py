from flask import Flask, request, send_file, jsonify, make_response
import os
import requests
from urllib.parse import urlparse
from src.translator import PotTranslator
from src.config import Config
import io

app = Flask(__name__)

def ensure_directories():
    """Ensure that upload and download directories exist."""
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.DOWNLOAD_FOLDER, exist_ok=True)

def download_file_from_url(url: str) -> str:
    """Download file from URL and save it locally."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Get filename from URL or use default
        filename = os.path.basename(urlparse(url).path)
        if not filename.endswith('.pot'):
            filename = 'downloaded.pot'
            
        ensure_directories()
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
            
        return file_path
    except Exception as e:
        raise ValueError(f"Failed to download file from URL: {str(e)}")

@app.route('/translate', methods=['POST'])
def translate():
    try:
        # Ensure directories exist
        ensure_directories()

        api_key = request.form.get('api_key')
        if not api_key:
            return jsonify({"error": "API key is required"}), 400

        # Remove quotes if they exist
        api_key = api_key.strip('"')
        
        model = request.form.get('model', Config.DEFAULT_MODEL)
        target_language = request.form.get('target_language', '').strip('"')
        if not target_language or len(target_language) != 2:
            return jsonify({"error": "Invalid target language format"}), 400

        file_url = request.form.get('file_url', '').strip('"')
        if file_url:
            # Завантаження файлу за URL
            try:
                input_path = download_file_from_url(file_url)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        else:
            # Звичайне завантаження файлу
            if 'file' not in request.files:
                return jsonify({"error": "No file provided and no file_url specified"}), 400

            file = request.files['file']
            if not file.filename.endswith('.pot'):
                return jsonify({"error": "Invalid file format"}), 400

            input_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)
            file.save(input_path)

        translator = PotTranslator(api_key=api_key, model=model)
        content, filename = translator.translate_pot_file(input_path, target_language)

        # Видаляємо вхідний файл
        try:
            os.remove(input_path)
        except:
            pass

        # Повертаємо файл як відповідь
        response = make_response(content)
        response.headers['Content-Type'] = 'application/x-gettext'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 