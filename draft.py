folder_number = ('img_1.jpg').split('_')[1].split('.')[0]  # Extract number from filename (e.g., "1" from "img_1.jpg")
    # image_files = sorted([f for f in os.listdir(image_folder) if f.startswith("img_") and f.endswith(".jpg")])
        
folder_name = f"DAI_{folder_number}"

print(folder_name)