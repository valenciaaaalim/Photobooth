
import requests
from dotenv import load_dotenv
load_dotenv()
import os 
import time

from test import shareable_link

webhook_url = os.getenv("NGROK_FORWARDING")
account_hash = os.getenv("USERAPI_HASH")
api_key = os.getenv('USERAPI_KEY')



def get_individual_image_urls(output_hash_id):
    #seed url 
    SEED_URL = "https://api.userapi.ai/midjourney/v2/seed"
    
    data = {
        "hash": output_hash_id,
        "is_async": False,
        "webhook_url": webhook_url,    
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    try:
        response = requests.post(SEED_URL, json=data, headers=headers)

        response.raise_for_status()  # Raises an error if the request failed
        data = response.json()

        if data.get("status") == "done" and "result" in data:
            return [img["url"] for img in data["result"]["urls"]]
        else:
            print("Error: API response incomplete.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def download_image(image_url, save_path):
    """
    Downloads an image from the provided URL and saves it locally.
    
    :param image_url: The URL of the image to download.
    :param save_path: The local file path to save the image.
    """
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image saved to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")

if __name__ == "__main__":

    image_urls = get_individual_image_urls('b6bdb904-1090-453d-b6d0-8c51fbc01deb')

    if image_urls:
        for i, url in enumerate(image_urls):
            print(f"Image {i+1}: {url}")

        # Download a specific image (e.g., image 2)
        image_number = 2  # Change this to select different images (1-4)
        if 1 <= image_number <= len(image_urls):
            download_image(image_urls[image_number - 1], f"midjourney_image_{image_number}.png")
    else:
        print("Failed to retrieve image URLs.")
        