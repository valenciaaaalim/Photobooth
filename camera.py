import cv2
import os

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
        return False, None
    

def stop_camera(cam_on, cam):
    if cam_on and cam is not None:
        cam.release()
        cam_on = False
        cv2.destroyAllWindows()
    print("Camera is now OFF")
    return cam_on, None


    
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
          print(f"Image saved to {img_path}")
          return img_path, img_id
      elif user_input == 'n':  # 'n'y for no to discard
          print("Image discarded.")
          break
      else:
          print("Invalid input. Please press 'y' to save or 'n' to discard.")
    return None, None



    
def main():
    cam_on, cam = False, None
    cam_on, cam= start_camera(cam_on, cam)
    print ("Press 'c' to snap a shot or 'q' to quit program")
    while True:
        ret, frame = cam.read()
        live = cv2.flip(frame,  1)
        cv2.imshow('Camera', live)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # cam_on, frame = capture_image(cam_on, cam)
            captured = cv2.flip(frame, 1)
            print("Press any key to close preview")
            cv2.waitKey(0)
            cv2.destroyWindow("Camera")
            cv2.waitKey(1)
            print("Closed preview")
            os.system("""osascript -e 'tell application "Visual Studio Code" to activate'""")
            img_path, img_id = accept_image(captured)
            return(img_path, img_id)
        elif key == ord('q'):
            print('Quitting program')
            print("Press any key to close preview")
            cv2.waitKey(0)
            cv2.destroyWindow("Camera")
            cv2.waitKey(1)
            print("Closed preview")
            os.system("""osascript -e 'tell application "Visual Studio Code" to activate'""")
            break
    stop_camera(cam_on, cam)
    return(None,None)
    



    