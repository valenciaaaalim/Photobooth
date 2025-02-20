import camera
import cloud
import imagineapi
import watermarking
from PIL import Image
import cv2
import asyncio

def capture_image():
  
  # capture image
  img_path, img_id = camera.main()
  if img_path and img_id:
    print('Camera done')
    print('Uploading to Drive...')

    # upload captured image to drive
    drive_link, folder_id, drive_img_id, qr_path = cloud.upload_original(img_path, img_id)
    print('Uploaded original image')
    return folder_id, drive_img_id, qr_path, img_id
  else:
     print('End of program')
     return None,None,None,None
  




async def flash_qr(qr_path):
    # flash qr code while printing
    qr_cv = cv2.imread(qr_path)
    cv2.imshow('QR', qr_cv)
    if qr_cv is not None:
        print('Displaying QR code until end of program.')  
        cv2.waitKey(1)  
        # Wait indefinitely until a key is pressed
    else:
        print("Error: Failed to load QR code image.")



      

async def generate_renaissance(drive_img_id, img_id, folder_id):
    # generate renaissance pictures from image then upload to drive
    # make the generation an async function
    midjourney_image_path = imagineapi.main(drive_img_id, img_id) # generation, will take about 1min
    # insert qr function
    print('Renaissance transformation done')


    # watermarking on renaissance image
    to_be_watermarked = Image.open(midjourney_image_path)
    watermarked_mj_path = watermarking.main(to_be_watermarked, img_id)
    print('Watermarking done')

    # upload watermarked renaissance image to drive
    cloud.upload_renaissance(watermarked_mj_path, folder_id)
    print('Uploaded final image onto Drive. Refresh Drive to view.')


    
    # printing will take 1.5min

async def main():
    
    folder_id, drive_img_id, qr_path, img_id = capture_image()
    if img_id is None:
       return
    else:
        await asyncio.gather(
           flash_qr(qr_path),
           generate_renaissance(drive_img_id, img_id, folder_id)
        )
        print('Press any key to close QR window')
        cv2.waitKey(0)
        cv2.destroyWindow('QR')
        cv2.waitKey(1)
        print('End of program. Start printing.')
        print('Next customer!')



if __name__ == "__main__":
    asyncio.run(main())