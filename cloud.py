from dotenv import load_dotenv
load_dotenv()
import os
import qrcode
import cv2
import requests
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from PIL import Image
from io import BytesIO
import numpy as np

# Authenticate Google Drive
def authenticate_google_drive():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")  # Load credentials if available

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("mycreds.txt")  # Save credentials for future use
    return GoogleDrive(gauth)


# Create folder in Google Drive
def create_drive_folder(drive, folder_name, parent_drive_folder_id=None):
    folder_metadata = {'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
    if parent_drive_folder_id:
        folder_metadata['parents'] = [{'id': parent_drive_folder_id}]

    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id']

# Upload image to Google Drive
def upload_file_to_drive(drive, file_path, folder_id):
    file_name = os.path.basename(file_path)
    file = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
    file.SetContentFile(file_path)
    file.Upload()
    return file['id']

# Generate a shareable Google Drive link
def get_shareable_link(drive, folder_id):
    folder = drive.CreateFile({'id': folder_id})
    folder.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
    return f"https://drive.google.com/drive/folders/{folder_id}"

# Generate and display QR Code
def generate_qr_code(link, img_id):
    print('Generating QR')
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    output_path= f"saved_img/{img_id}_QR.png"
    img.save(output_path)
    print('QR code saved successfully.')
    # qr_img = Image.open(output_path)
    
    

    # Load image numpy with OpenCV
    qr_cv = cv2.imread(output_path)
    cv2.imshow('QR', qr_cv)
    if qr_cv is not None:
        print('Displaying QR code...press any key to close image and continue to generation')        
        # Wait indefinitely until a key is pressed
        key = cv2.waitKey(0)
        print(f"Key pressed: {key}")  # Debugging
        # Close all OpenCV windows
        cv2.destroyAllWindows()
        cv2.waitKey(1) #to properly wait until destroyAllWindows is effective
    else:
        print("Error: Failed to load QR code image.")

# Main function
def upload_original(img_path, img_id):
    parent_drive_folder_id = os.getenv("DRIVE_PARENT_FOLDER")
    drive = authenticate_google_drive()
    # folder_number = img_path.split('_')[1].split('.')[0]  # Extract number from filename (e.g., "1" from "img_1.jpg")
    # # image_files = sorted([f for f in os.listdir(image_folder) if f.startswith("img_") and f.endswith(".jpg")])
        
    folder_name = f"DAI_{img_id}"  # Google Drive folder name

    # Create Google Drive folder
    folder_id = create_drive_folder(drive, folder_name, parent_drive_folder_id)

    # Upload original image
    # image_path = os.path.join(image_folder, image_file)
    drive_img_id = upload_file_to_drive(drive, img_path, folder_id)

    # Get shareable link & generate QR code
    drive_link = get_shareable_link(drive, folder_id)
    generate_qr_code(drive_link, img_id)

    print(f"Folder {folder_name} created. QR Code generated! Shareable link: {drive_link}")

    return drive_link, folder_id, drive_img_id


def upload_renaissance(img_path, folder_id):
    drive = authenticate_google_drive()
    upload_file_to_drive(drive, img_path, folder_id)
    

