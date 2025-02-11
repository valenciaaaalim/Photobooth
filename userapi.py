import requests
from dotenv import load_dotenv
load_dotenv()
import os 
import time

from test import shareable_link

webhook_url = os.getenv("NGROK_FORWARDING")
account_hash = os.getenv("USERAPI_HASH")
api_key = os.getenv('USERAPI_KEY')


def get_direct_drive_img(url):
  id = url.split('d/')[1].split('/view?')[0]
  print(id)
  google_drive_image_url = "https://drive.google.com/uc?export=view&id="+ str(id)
  print(google_drive_image_url)
  return google_drive_image_url
 
def generate_prompt(gender):
    if gender.lower() == 'm':
        return "this is a hyperrealistic renaissance oil painting of the same rich and handsome man in the renaissance era, against a black studio wall. He has the same face and is dressed in medieval European renaissance style royal attire, bright intense eyes, half body portrait, same skin tone, dignified posture, rich details. The painting has a warm lighting with high contrast, dark background and warm glow on the person as the focus of the painting. --ar 21:34"
    elif gender.lower() == 'f':
        return "this is a hyperrealistic renaissance oil painting of the same rich and beautiful woman in the renaissance era, against a black studio wall. She has the same face and is dressed in medieval European renaissance style royal attire, bright intense eyes, delicate skin, half body portrait, same skin tone, elegant posture, rich details. The painting has a warm lighting with high contrast, dark background and warm glow on the person as the focus of the painting. --ar 21:34"
    else:
      return None
    
def get_gender_input():
    while True:
        gender = input("Enter the gender (m/f): ").lower()
        if gender in ['m', 'f']:
            return gender
        else:
            print("Invalid input! Please enter 'm' or 'f'.")


def post_request():
    # Set the request URL
    imagine_url = "https://api.userapi.ai/midjourney/v2/imagine"
    
    # Define the request payload (JSON body)
    data = {
        "prompt": f"{img_url} {prompt}",
        "webhook_url": webhook_url,  
        "webhook_type": "progress",  
        "account_hash": account_hash,
        "is_disable_prefilter": False
    }

    # Set the request headers (authentication)
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    # Send the POST request to the API
    response = requests.post(imagine_url, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        task_hash = response_data.get("hash")
        print(f"Task hash: {task_hash}")
    else:
        print(f"Error: {response.text}")




def get_individual_image_urls():
    #seed url 
    SEED_URL = "https://api.userapi.ai/midjourney/v2/seed"
    
    payload = {
        "account_hash": account_hash,
        "is_async": False,
        "webhook_url": webhook_url,  
        "webhook_type": "progress",  
    }

    try:
        response = requests.post(SEED_URL, json=payload)
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
    # Example usage
    hash_id = "c9475420-688b-43e3-941b-7bd2fedaf17f"  # Replace with your actual hash
    image_urls = get_individual_image_urls(hash_id)

    if image_urls:
        for i, url in enumerate(image_urls):
            print(f"Image {i+1}: {url}")

        # Download a specific image (e.g., image 2)
        image_number = 2  # Change this to select different images (1-4)
        if 1 <= image_number <= len(image_urls):
            download_image(image_urls[image_number - 1], f"midjourney_image_{image_number}.png")
    else:
        print("Failed to retrieve image URLs.")
        
        
# Take user input for gender
img_url = get_direct_drive_img(shareable_link)
gender = get_gender_input()
prompt = generate_prompt(gender)