import json
import time
import http.client
import pprint
import os
from dotenv import load_dotenv
load_dotenv()
import requests

api_key = os.getenv('IMAGINEAPI_KEY')


def get_direct_drive_img(drive_img_id):
  #id = url.split('d/')[1].split('/view?')[0]
  #print(drive_img_id)
  google_drive_image_url = "https://drive.google.com/uc?export=view&id="+ str(drive_img_id)
  #print(google_drive_image_url)
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
        return "this is a hyperrealistic renaissance oil painting of the same rich and beautiful woman in the renaissance era, against a black studio wall. She has the same face and is dressed in medieval European renaissance style modest royal attire, bright intense eyes, delicate skin, half body portrait, same skin tone, elegant posture, rich details. Modest attire. The painting has a warm lighting with high contrast, dark background and warm glow on the person as the focus of the painting. --ar 21:34"
    elif gender.lower()== 'group':
        return "this is a hyperrealistic renaissance oil painting of the same rich and good-looking people in the renaissance era, against a black studio wall. They are dressed in medieval European renaissance style royal attire, bright intense eyes, delicate skin, half body portrait, same skin tone, elegant posture, rich details. The painting has a warm lighting with high contrast, dark background and warm glow on the people as the focus of the painting. --ar 21:34"




headers = {
    'Authorization': F"Bearer {api_key}",  # <<<< TODO: remember to change this
    'Content-Type': 'application/json'
}

def body(img_url, prompt):
    data = {"prompt": f"{img_url} {prompt}"}
    return data
 




def send_request(method, path, body=None, headers={}):
    conn = http.client.HTTPSConnection("cl.imagineapi.dev")
    conn.request(method, path, body=json.dumps(body) if body else None, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode())
    conn.close()
    return data




 
def check_image_status(prompt_response_data):
    response_data = send_request('GET', f"/items/images/{prompt_response_data['data']['id']}", headers=headers)
    if response_data['data']['status'] in ['completed', 'failed']:
        print('Completed image details',)
        #pprint.pp(response_data['data'])
        chosen_url = response_data['data']['upscaled_urls'][0]
        #pprint.pp(response_data['data']['upscaled_urls'][0])
        return True, chosen_url
    else:
        print(f"Image is not finished generation. Status: {response_data['data']['status']}")
        return False
 




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







def main(drive_img_id, img_id):
    img_url = get_direct_drive_img(drive_img_id)
    os.system("""osascript -e 'tell application "Visual Studio Code" to activate'""")
    gender = get_gender_input()
    prompt = generate_prompt(gender)
    data = body(img_url, prompt)
    prompt_response_data = send_request('POST', '/items/images/', data, headers)
    pprint.pp(prompt_response_data)
    while not check_image_status(prompt_response_data):
        time.sleep(5)  # wait for 5 seconds
    status, chosen_url = check_image_status(prompt_response_data)
    #print(chosen_url)
    midjourney_image_path = os.path.join("saved_img",f"{img_id}_notWatermarked.jpg")
    download_image(chosen_url, midjourney_image_path)
    return midjourney_image_path
