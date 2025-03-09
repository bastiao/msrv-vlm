import google.generativeai as genai
import base64
import os

class VLMAnalyzer:
    def __init__(self, api_key):
        genai.configure(api_key=api_key, transport="rest")
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_text_with_image(self, prompt, image_path):
        """Generates text from an image and a text prompt."""
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            encoded_image = base64.b64encode(image_data).decode("utf-8")

        image_part = {
            "mime_type": "image/jpeg",  # Adjust mime type if necessary
            "data": encoded_image
        }

        response = self.model.generate_content([prompt, image_part])
        return response.text

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python vlm.py <api_key> <prompt> <image_path>")
        sys.exit(1)

    api_key = sys.argv[1]
    prompt = sys.argv[2]
    image_path = sys.argv[3]

    analyzer = VLMAnalyzer(api_key)
    result = analyzer.generate_text_with_image(prompt, image_path)
    print(result)