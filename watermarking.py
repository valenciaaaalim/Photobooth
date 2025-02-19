from PIL import Image
import os
import cv2
import numpy as np

def main(image,img_id):
    watermark = 'watermark_white.png'
    watermark = Image.open(watermark)
    watermark = watermark.convert('RGBA')  # Convert watermark to RGBA

    # Resize watermark to make it smaller
    wm_width, wm_height = watermark.size
    new_width = wm_width //4   # Resize to 25% of the original width
    new_height = wm_height //4   # Resize to 25% of the original height
    watermark = watermark.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Ensure the base image is in RGBA to match the watermark (preserves transparency)
    image = image.convert('RGBA')

    # Get the width and height of the base image
    img_width, img_height = image.size

    # Calculate the position for the watermark at the bottom-left corner
    x_position = 35  # Align to the left
    y_position = img_height - new_height - 30 # Position at the bottom

    # Paste watermark onto the image (third argument is the watermark's alpha channel for transparency)
    image.paste(watermark, (x_position, y_position), watermark)  # Use watermark as mask for transparency
    watermarked_image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)
    img_path = os.path.join("saved_img",f"{img_id}_Renaissance.jpg")
    cv2.imwrite(img_path, watermarked_image_cv)
    print(f"Image saved to {img_path}")

    return img_path

# # Load the main image
# mj = Image.open('saved_img/10_Renaissance.jpg')
# image = main(mj)

# # Convert the result back to OpenCV format for display
# watermarked_image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)

# # Display the watermarked image
# cv2.imshow('watermarked', watermarked_image_cv)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
