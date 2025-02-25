from dotenv import load_dotenv
load_dotenv()
import os
import qrcode
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import cv2

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
    print('Generating QR...')
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    output_path= f"saved_img/{img_id}_QR_unlabelled.png"
    img.save(output_path)
    
    qr_updated = cv2.imread(output_path)
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Blue color in BGR
    color = (0, 0, 0)
    # Line thickness of 2 px
    thickness = 1

    qr_updated = cv2.copyMakeBorder(qr_updated, 20, 40, 0, 0, cv2.BORDER_WRAP)
    # Using cv2.putText() method
    qr_updated = cv2.putText(qr_updated, 'Save a picture of this to see your transformation!', (40,40), font, 
                      0.5, color, thickness, cv2.LINE_AA)

    qr_updated = cv2.putText(qr_updated, 'Disclaimer: This is a fun activity to transform us into the' , (45,470), font, 
                      0.4, color, thickness, cv2.LINE_AA)
    qr_updated = cv2.putText(qr_updated, 'Medieval Western European era. Refresh after a while.' , (45,490), font, 
                      0.4, color, thickness, cv2.LINE_AA) 
    # qr_updated = cv2.putText(qr_updated, 'You will look like a Westerner from that period.' , (45,510), font, 
    #                   0.4, color, thickness, cv2.LINE_AA) 

    output_path= f"saved_img/{img_id}_QR.png"
    cv2.imwrite(output_path,qr_updated)
    

    print('QR code saved locally')
    return output_path
    


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
    qr_path = generate_qr_code(drive_link, img_id)

    print(f"Folder {folder_name} created on Drive. Shareable link: {drive_link}")

    return drive_link, folder_id, drive_img_id, qr_path


def upload_renaissance(img_path, folder_id):
    drive = authenticate_google_drive()
    upload_file_to_drive(drive, img_path, folder_id)
    

