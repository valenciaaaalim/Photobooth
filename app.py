import camera
import cloud
import imagineapi

def main():
  img_path, img_id = camera.main()
  print('camera done')
  drive_link, folder_id, drive_img_id = cloud.upload_original(img_path, img_id)
  print('uploading original done')
  midjourney_image_path = imagineapi.main(drive_img_id, img_id)
  print('renaissance transformation done')
  cloud.upload_renaissance(midjourney_image_path, folder_id)
  print('uploading renaissance done')





if __name__ == "__main__":
    main()