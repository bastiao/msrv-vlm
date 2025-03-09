from flask import Flask, request, jsonify
import os
from PIL import Image
import io
from vlm_analysis.vlm import VLMAnalyzer
from dotenv import load_dotenv

class VLMApp:
    def __init__(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.api_key = os.getenv("GEMINI_API_KEY")
        print("API Key:", self.api_key)
        if not self.api_key:
            raise ValueError("No GEMINI_API_KEY environment variable set")
        
        self.analyzer = VLMAnalyzer(self.api_key)
        self.UPLOAD_FOLDER = '_uploads'
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)
        self.app.config['UPLOAD_FOLDER'] = self.UPLOAD_FOLDER
        self.DEFAULT_PROMPT = "This is an imaging from digital pathology. Tell me what are the organ and staining type. Return in JSON Format"
        
        self.app.add_url_rule('/upload', 'upload_file', self.upload_file, methods=['POST'])

    def upload_file(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and self.allowed_file(file.filename):
            filename = os.path.join(self.app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            print("File saved as", filename)  
            try:
                print("Analyzing image...")
                prompt = request.form.get('prompt', self.DEFAULT_PROMPT)
                result = self.analyze_image(filename, prompt)
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': str(e)})

        else:
            return jsonify({'error': 'Invalid file type. Only JPEG allowed.'})

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

    def analyze_image(self, image_path, prompt):
        try:
            result = self.analyzer.generate_text_with_image(prompt, image_path)
            return result
        except Exception as e:
            raise Exception(f"Error analyzing image: {e}")

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    vlm_app = VLMApp()
    vlm_app.run()