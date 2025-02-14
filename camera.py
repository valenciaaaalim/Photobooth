import cv2
import os
from PIL import Image
import io
from AppKit import NSPasteboard, NSPasteboardTypePNG
from Foundation import NSData

def start_camera(cam_on, cam):
    cam = cv2.VideoCapture(0)
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if cam.isOpened():
      cam_on = True
      print("Camera is now ON")
      return cam_on, cam
    elif not cam.isOpened():
        cam_on = False
        print("Error: Unable to access the camera.")
        return False, None, frame_width, frame_height
    

def stop_camera(cam_on, cam):
    if cam_on and cam is not None:
        cam.release()
        cam_on = False
        cv2.destroyAllWindows()
    print("Camera is now OFF")
    return cam_on, None


def send_to_clipboard(img):
    # Convert OpenCV image (BGR) to PIL image (RGB)
    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Save image to a bytes buffer as PNG
    output = io.BytesIO()
    image.save(output, format="PNG")
    image_data = output.getvalue()

    # Convert image data to NSData (macOS format)
    ns_data = NSData.dataWithBytes_length_(image_data, len(image_data))

    # Access the macOS clipboard
    pasteboard = NSPasteboard.generalPasteboard()
    pasteboard.clearContents()  # Clear existing clipboard content

    # Write the image data to clipboard in PNG format
    pasteboard.setData_forType_(ns_data, NSPasteboardTypePNG)



def capture_image(cam_on, cam):
    # cam_on, cam = start_camera(cam_on, cam)
    ret, frame = cam.read()
    if not ret:
        print("Error: Unable to capture image.")
        return
    elif ret:
        cv2.imshow("Preview", frame)
        print("Press any key to close preview")
        cv2.waitKey(0)
        cv2.destroyWindow("Preview")
        cv2.waitKey(1)
        print("destroyWindow")
        cam_on = False
        # waiting for any keypress, then will close window
        os.system("""osascript -e 'tell application "Visual Studio Code" to activate'""")
        return cam_on, frame
    

    
def get_next_filename():
    # Start numbering from 1 and keep checking the filenames
    i = 1
    while os.path.exists(os.path.join("saved_img", f"{i}_Img.jpg")):
        i += 1
    img_id = i
    return os.path.join("saved_img",f"{i}_Img.jpg"), img_id  # Return the next available filename



def accept_image(frame):
    print("Press 'y' to save or 'n' to discard the image.")
    while True:
      user_input = input("Save the image? (y/n): ").strip().lower()
      if user_input == 'y':  # 'y' for yes to save
          img_path, img_id = get_next_filename()
          print(img_path)
          cv2.imwrite(img_path, frame)
          print(f"Image saved to {img_path} and clipboard")
          break
      elif user_input == 'n':  # 'n'y for no to discard
          print("Image discarded.")
          break
      else:
          print("Invalid input. Please press 'y' to save or 'n' to discard.")
    return img_path, img_id



    
def main():
    cam_on, cam = False, None
    cam_on, cam= start_camera(cam_on, cam)
    print ("Press 'c' to snap a shot or 'q' to quit program")
    while True:
        ret, frame = cam.read()
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) == ord('c'):
            cam_on, frame = capture_image(cam_on, cam)
            img_path, img_id = accept_image(frame)
            break
        elif cv2.waitKey(1) == ord('q'):
            break
    stop_camera(cam_on, cam)
    return(img_path, img_id)



    