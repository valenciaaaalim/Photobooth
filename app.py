import camera
import cloud
import print
import imagineapi

def main():
  img_path, img_id = camera.main()
  drive_link, folder_id = cloud.upload_original(img_path, img_id)
  midjourney_image_path = imagineapi.main(drive_link, img_id)
  cloud.upload_renaissance(midjourney_image_path, folder_id)






if __name__ == "__main__":
    main()