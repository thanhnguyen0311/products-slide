import pandas as pd
from collections import defaultdict


def read_excel_data(file_path):
    try:
        df = pd.read_excel(file_path)

        print(df.columns)

        df.columns = ['Sheet Order', 'SKU', 'Image Src', 'Image Position']

        # Create a dictionary to store objects and their images
        objects_dict = defaultdict(list)

        for _, row in df.iterrows():
            object_name = row['SKU']
            image_link = row['Image Src']
            objects_dict[object_name].append(image_link)

        print(f"Successfully read {len(objects_dict)} products from Excel file")

        for i, (obj_name, images) in enumerate(objects_dict.items()):
            if i >= 2:  # Only show first 2 objects
                break
            print(f"\nObject: {obj_name}")
            print("Images:")
            for idx, img_link in enumerate(images, 1):
                print(f"{idx}. {img_link}")

        return objects_dict

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        return None