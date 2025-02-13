
import requests
from dotenv import load_dotenv
load_dotenv()
import os 
import time
import json
import http.client
import pprint

from test import shareable_link

webhook_url = os.getenv("NGROK_FORWARDING")
account_hash = os.getenv("USERAPI_HASH")
api_key = os.getenv('USERAPI_KEY')



def get_chosen_img_url(output_hash_id):
    #seed url 
    SEED_URL = "https://api.userapi.ai/midjourney/v2/upsample"

    data = {
        "hash": output_hash_id,
        "is_async": False,
        "webhook_url": webhook_url,    
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    response = requests.post(SEED_URL, json=data, headers=headers)
    output = response.json()
    # print("Raw Response Text:", response.text)
    # print("Raw Response Status Code:", response.status_code)
    # print('type of object:', type(response))
    #data = json.loads(response.read().decode())
    print(type(output))
    pprint.pp(output, indent=4)

    # Check if the request was successful
    if response.status_code == 200:
        print('success')
        # with open(response) as f:
        #     dict = json.load(f)
        #     chosen_url = dict.get('result').get('urls')[3].get('url')
    #return chosen_url

      
def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image saved to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")




chosen_img = get_chosen_img_url('d5aac892-5a04-4ca8-ab9c-566fc735d9bd') #replace this with the unused hash of the imagine job
print('the chosen img url is:', chosen_img)
download_image(chosen_img, f"mj_1234.png")
    
        

#5ecf8e08-0b28-44fe-8b56-6de98055c1ff
#c9475420-688b-43e3-941b-7bd2fedaf17f
#af0b4520-7ea6-46c7-bfa9-51c285d58c61
#b6bdb904-1090-453d-b6d0-8c51fbc01deb
#d5ab4851-3f81-4a15-9e9e-54138e3e84e8
#95bb2c8b-454a-49cb-a420-f539acc219d0
#a9480985-1358-426f-b979-e94a2bc73c45
#8ed4b303-e8a1-4bb4-9a71-3ad8fe208e72
#fd6eb070-85e3-4fc5-98fc-8057652848a2
#d5aac892-5a04-4ca8-ab9c-566fc735d9bd