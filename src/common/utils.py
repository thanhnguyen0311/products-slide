import pandas as pd
from collections import defaultdict
from src.models.Product import Product


def read_excel_data(file_path):
    try:
        df = pd.read_excel(file_path)

        df.columns = ['Sheet Order', 'SKU', 'Image Src', 'Image Position']

        # Create a dictionary to store objects and their images
        objects_dict = defaultdict(list)

        for _, row in df.iterrows():
            object_name = row['SKU']
            image_link = row['Image Src']
            objects_dict[object_name].append(image_link)

        product_list = []

        max_iterations = 3  # Set the limit for the loop
        count = 0  # Initialize a counter

        for sku, images in objects_dict.items():
            product_list.append(Product(sku=sku, images=images))
            count += 1
            if count >= max_iterations:
                break  # Exit the loop after 3 iterations

        print(f"Successfully read {len(product_list)} products from Excel file")
        # for idx, product in enumerate(product_list, 1):
        #
        #     if idx >= 3:  # Only show first 2 objects
        #         break
        #     product.__str__()

        return product_list

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        return None
