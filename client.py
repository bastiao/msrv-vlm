import requests
import json
import argparse

def upload_image(image_path, prompt, api_url="http://127.0.0.1:5000/upload"):
    """
    Uploads an image and a prompt to the specified API and prints the JSON response.

    Args:
        image_path (str): The path to the image file.
        prompt (str): The prompt to be sent with the image.
        api_url (str): The URL of the API endpoint.
    """
    try:
        with open(image_path, 'rb') as image_file:
            files = {'file': (image_path.split('/')[-1], image_file, 'image/png')}
            data = {'prompt': prompt}
            response = requests.post(api_url, files=files, data=data)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            print(json.dumps(response.json(), indent=4)) # Pretty-print the JSON response
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed: {e}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON response from API: {response.text}") # Print the text of the response.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload an image and a prompt to the specified API and print the JSON response.")
    parser.add_argument('image_path', type=str, help="The path to the image file.")
    parser.add_argument('prompt', type=str, help="The prompt to be sent with the image.")
    parser.add_argument('api_url', type=str, nargs='?', default="http://127.0.0.1:5000/upload", help="The URL of the API endpoint.")
    
    args = parser.parse_args()
    
    upload_image(args.image_path, args.prompt, args.api_url)