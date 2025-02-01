import cv2
import os 
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

def start_camera(cam_on, cam):
    cam = cv2.VideoCapture(0)
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
    print("Camera is now OFF")
    return cam_on, None


def capture_image(cam_on, cam):
    cam_on, cam = start_camera(cam_on, cam)
    ret, frame = cam.read()
    if not ret:
        print("Error: Unable to capture image.")
        return
    elif ret:
        cv2.imshow("Preview", frame)
        print("waitKey not yet responded")
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
    while os.path.exists(f"img_{i}.jpg"):
        i += 1
    return f"img_{i}.jpg"  # Return the next available filename

def accept_image(frame):
    print("Press 'y' to save or 'n' to discard the image.")
    while True:
      user_input = input("Save the image? (y/n): ").strip().lower()
      if user_input == 'y':  # 'y' for yes to save
          img_path = get_next_filename()
          cv2.imwrite(img_path, frame)
          print(f"Image saved to {img_path}")
          break
      elif user_input == 'n':  # 'n'y for no to discard
          print("Image discarded.")
          break
      else:
          print("Invalid input. Please press 'y' to save or 'n' to discard.")
    


def main():
    cam_on, cam = False, None
    print("Press 'c' to capture an image")
    while True:
        command = input("Enter a command: ").strip().lower()
        if command == 'c':
          cam_on, frame = capture_image(cam_on, cam)
          accept_image(frame)
        else:
            print("Invalid command, only 'c' or quit program, with ctrl+c")
        if cam_on and cam is not None:
          cam.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)


main()
    

def camera_program():
    cam_on = False  # Camera starts off
    cam = None      # Camera object

    print("Commands:")
    print("  'start' - Turn camera ON")
    print("  'stop' - Turn camera OFF")
    print("  'c' - Capture an image (only when camera is ON)")
    print("  'quit' - Exit the program")

    while True:
        command = input("Enter a command: ").strip().lower()

        if command == 'start':
            if not cam_on:
                cam = cv2.VideoCapture(0)  # Turn camera on
                if not cam.isOpened():
                    print("Error: Unable to access the camera.")
                    cam = None
                else:
                    cam_on = True
                    print("Camera is now ON")
            else:
                print("Camera is already ON")

        elif command == 'stop':
            if cam_on and cam is not None:
                cam.release()  # Turn camera off
                cam_on = False
                print("Camera is now OFF")
            else:
                print("Camera is already OFF")

        elif command == 'c':
            if cam_on and cam is not None:
                ret, frame = cam.read()  # Capture a frame
                if ret:
                    cv2.imshow("Preview", frame)
                    cv2.waitKey(1)
                    os.system("""osascript -e 'tell application "Visual Studio Code" to activate'""")
                    print("Press 'y' to save or 'n' to discard the image.")
                    while True:
                        user_input = input("Save the image? (y/n): ").strip().lower()
                        #cv2.waitKey(0)
                        if user_input == 'y':  # 'y' for yes to save
                            img_path = get_next_filename()
                            cv2.imwrite(img_path, frame)
                            print(f"Image saved to {img_path}")
                            break
                        elif user_input == 'n':  # 'n'y for no to discard
                            print("Image discarded.")
                            break
                        else:
                            print("Invalid input. Please press 'y' to save or 'n' to discard.")
                else:
                    print("Error: Unable to capture image.")
            else:
                print("Camera is not ON. Use 'start' to turn it ON.")

            # cv2.destroyAllWindows()  # Close the preview window
            # os.system("""osascript -e 'tell application "System Events" to keystroke "j" using {command down}'""")
            # os.system("""osascript -e 'tell application "System Events" to keystroke "j" using {command down}'""")

        elif command == 'quit':
            print("Exiting program.")
            break

        else:
            print("Invalid command. Try 'start', 'stop', 'c', or 'quit'.")

    # Release resources if the camera is still on
    if cam_on and cam is not None:
        cam.release()
    cv2.destroyAllWindows()



#check if camera on
# if camera on, turn  it off then call start camera function


    cam = cv2.VideoCapture(0)
    if cam.isOpened():
        ret,frame = cam.read()
    else:
        ret = False
    while ret:
        cv2.imshow("camera")