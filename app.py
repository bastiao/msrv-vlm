from flask import Flask, request, jsonify
import os
from PIL import Image
import io
from vlm_analysis.vlm import VLMAnalyzer

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure your Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
print("API Key:", api_key)
if not api_key:
    raise ValueError("No GEMINI_API_KEY environment variable set")

analyzer = VLMAnalyzer(api_key)

UPLOAD_FOLDER = '_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DEFAULT_PROMPT = "This is an imaging from digital pathology. Tell me what are the organ and staining type. Return in JSON Format"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        print("File saved as", filename)  
        try:
            print("Analyzing image...")
            prompt = request.form.get('prompt', DEFAULT_PROMPT)
            result = analyze_image(filename, prompt)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})

    else:
        return jsonify({'error': 'Invalid file type. Only JPEG allowed.'})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

def analyze_image(image_path, prompt):
    try:
        result = analyzer.generate_text_with_image(prompt, image_path)
        return result
    except Exception as e:
        raise Exception(f"Error analyzing image: {e}")

if __name__ == '__main__':
    app.run(debug=True)