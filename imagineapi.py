import http.client
import json
import pprint
from dotenv import load_dotenv
load_dotenv()
import os
import time
import requests

api_key = os.getenv('IMAGINEAPI_TOKEN')



def get_direct_drive_img(url):
  id = url.split('d/')[1].split('/view?')[0]
  print(id)
  google_drive_image_url = "https://drive.google.com/uc?export=view&id="+ str(id)
  print(google_drive_image_url)
  return google_drive_image_url
 
def get_gender_input():
    while True:
        gender = input("Enter the gender (m/f/group): ").lower()
        if gender in ['m', 'f', 'group']:
            return gender
        else:
            print("Invalid input! Please enter 'm' or 'f' or 'group'.")

def generate_prompt(gender):
    if gender.lower() == 'm':
        return "this is a hyperrealistic renaissance oil painting of the same rich and handsome man in the renaissance era, against a black studio wall. He has the same face and is dressed in medieval European renaissance style royal attire, bright intense eyes, half body portrait, same skin tone, dignified posture, rich details. The painting has a warm lighting with high contrast, dark background and warm glow on the person as the focus of the painting. --ar 21:34"
    elif gender.lower() == 'f':
        return "this is a hyperrealistic renaissance oil painting of the same rich and beautiful woman in the renaissance era, against a black studio wall. She has the same face and is dressed in medieval European renaissance style royal attire, bright intense eyes, delicate skin, half body portrait, same skin tone, elegant posture, rich details. The painting has a warm lighting with high contrast, dark background and warm glow on the person as the focus of the painting. --ar 21:34"
    elif gender.lower()== 'group':
        return "this is a hyperrealistic renaissance oil painting of the same rich and good-looking people in the renaissance era, against a black studio wall. They are dressed in medieval European renaissance style royal attire, bright intense eyes, delicate skin, half body portrait, same skin tone, elegant posture, rich details. The painting has a warm lighting with high contrast, dark background and warm glow on the people as the focus of the painting. --ar 21:34"





headers = {
    'Authorization': F"Bearer {api_key}",  # <<<< TODO: remember to change this
    'Content-Type': 'application/json'
}


def post_request(img_url,prompt, headers=headers):
    payload = {
        "prompt": f"{img_url} {prompt}",
    }
 
    conn = http.client.HTTPSConnection("cl.imagineapi.dev")
    conn.request("POST", "/items/images/", body=json.dumps(payload), headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode())
    conn.close()
    pprint.pp(data)
    return data

 
def check_image_status(data, completion):
    response_data = post_request('GET', f"/items/images/{data['data']['id']}", headers=headers)
    #status is False
    if response_data['data']['status'] in ['completed', 'failed']:
        print('Completed image details',)
        pprint.pp(response_data['data'])
        print(type(response_data))
        print(type(response_data['data']))
        chosen_url = response_data['data']['upscaled_urls'][3]
        print('Chosen url:' , chosen_url)
        return chosen_url, completion == True
    else:
    #status is Positive
        print(f"Image is not finished generation. Status: {response_data['data']['status']}")
        return None, completion == False
    




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




 
def main(drive_link, img_id):
    img_url = get_direct_drive_img(drive_link)
    print('img url obtained')
    gender = get_gender_input()
    print('gender obtained')
    
    prompt = generate_prompt(gender)
    data = post_request(img_url,prompt)
    status = False
    while not status:
      chosen_url, status = check_image_status(data, status)
      time.sleep(5)
    midjourney_image_path = os.path.join("saved_img",f"renaissance_{img_id}.jpg")
    download_image(chosen_url, midjourney_image_path)
    return midjourney_image_path
  


