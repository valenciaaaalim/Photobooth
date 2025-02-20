from PIL import Image
import os
import cv2
import numpy as np

def main(image,img_id):
    
    # Ensure the base image is in RGBA to match the watermark (preserves transparency)
    image = image.convert('RGBA')
    img_width, img_height = image.size


    # sutd watermark
    sutd = 'watermark_white.png'
    sutd = Image.open(sutd)
    sutd = sutd.convert('RGBA')  # Convert watermark to RGBA

    # Resize watermark to make it smaller
    sutd_width, sutd_height = sutd.size
    downsized_sutd_width = sutd_width //5   # Resize to 25% of the original width
    downsized_sutd_height = sutd_height //5   # Resize to 25% of the original height
    sutd = sutd.resize((downsized_sutd_width, downsized_sutd_height), Image.Resampling.LANCZOS)


    # Calculate the position for the watermark at the bottom-left corner
    x_position = 35
    y_position = img_height - downsized_sutd_height - 30

    # Paste watermark onto the image (third argument is the watermark's alpha channel for transparency)
    image.paste(sutd, (x_position, y_position), sutd)  # Use watermark as mask for transparency




    # credit wawtermark
    credit = 'credit_white.png'
    credit = Image.open(credit)
    credit = credit.convert('RGBA')  # Convert watermark to RGBA

    # Resize watermark to make it smaller
    credit_width, credit_height = credit.size
    downsized_credit_width = credit_width //5   # Resize to 25% of the original width
    downsized_credit_height = credit_height //5   # Resize to 25% of the original height
    credit = credit.resize((downsized_credit_width, downsized_credit_height), Image.Resampling.LANCZOS)

    # Get the width and height of the base image
    img_width, img_height = image.size

    # Calculate the position for the watermark at the bottom-left corner
    x_position = img_width - downsized_credit_width - 35  # Align to the left
    y_position = img_height - downsized_credit_height - 30 # Position at the bottom

    # Paste watermark onto the image (third argument is the watermark's alpha channel for transparency)
    image.paste(credit, (x_position, y_position), credit)  # Use watermark as mask for transparency






    watermarked_image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)
    img_path = os.path.join("saved_img",f"{img_id}_Renaissance.jpg")
    cv2.imwrite(img_path, watermarked_image_cv)
    print(f"Image saved to {img_path}")

    return img_path

