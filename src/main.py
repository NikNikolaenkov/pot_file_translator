from flask import Flask, request, send_file, jsonify
import os
from src.translator import PotTranslator
from src.config import Config

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        api_key = request.form.get('api_key')
        if not api_key:
            return jsonify({"error": "API key is required"}), 400

        model = request.form.get('model', Config.DEFAULT_MODEL)
        target_language = request.form.get('target_language')
        if not target_language or len(target_language) != 2:
            return jsonify({"error": "Invalid target language format"}), 400

        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if not file.filename.endswith('.pot'):
            return jsonify({"error": "Invalid file format"}), 400

        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        input_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        translator = PotTranslator(api_key=api_key, model=model)
        output_file = translator.translate_pot_file(input_path, target_language)

        return send_file(
            output_file,
            as_attachment=True,
            download_name=f"{target_language}.po"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 