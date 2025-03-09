import google.generativeai as genai
import base64
import os
import json

class VLMAnalyzer:
    def __init__(self, api_key):
        genai.configure(api_key=api_key, transport="rest")
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_text_with_image(self, prompt, image_path, return_format="json"):
        """Generates text from an image and a text prompt."""
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            encoded_image = base64.b64encode(image_data).decode("utf-8")

        image_part = {
            "mime_type": "image/jpeg",  # Adjust mime type if necessary
            "data": encoded_image
        }

        response = self.model.generate_content([prompt, image_part])
        
        if return_format.lower() == "json":
            return self.convert_to_json(response.text)
        elif return_format.lower() == "json-ld":
            return self.convert_to_json_ld(response.text)
        else:
            raise ValueError(f"Unsupported return format: {return_format}")

    def convert_to_json(self, response_text):
        try:
            # Remove Markdown code block indicators
            cleaned_response = response_text.strip().strip('```json').strip('```')
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            raise ValueError("Failed to decode response as JSON")

    def convert_to_json_ld(self, response_text):
        try:
            cleaned_response = response_text.strip().strip('```json').strip('```')
            json_content = json.loads(cleaned_response)
            return {
                "@context": "http://schema.org",
                "@type": "ImageObject",
                "content": json_content
            }
        except json.JSONDecodeError:
            raise ValueError("Failed to decode response as JSON-LD")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: python vlm.py <api_key> <prompt> <image_path> <return_format>")
        sys.exit(1)

    api_key = sys.argv[1]
    prompt = sys.argv[2]
    image_path = sys.argv[3]
    return_format = sys.argv[4]

    analyzer = VLMAnalyzer(api_key)
    result = analyzer.generate_text_with_image(prompt, image_path, return_format)
    print(json.dumps(result, indent=2))