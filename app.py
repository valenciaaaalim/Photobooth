import camera
import cloud
import imagineapi
import watermarking
from PIL import Image

def main():
  img_path, img_id = camera.main()
  if img_path and img_id:
    print('camera done')
    drive_link, folder_id, drive_img_id = cloud.upload_original(img_path, img_id)
    print('uploading original done')
    midjourney_image_path = imagineapi.main(drive_img_id, img_id)
    print('renaissance transformation done')
    to_be_watermarked = Image.open(midjourney_image_path)
    watermarked_mj_path = watermarking.main(to_be_watermarked, img_id)
    print('watermarking done')
    cloud.upload_renaissance(watermarked_mj_path, folder_id)
    print('uploading renaissance done')
  else:
     print('End of prgram')





if __name__ == "__main__":
    main()