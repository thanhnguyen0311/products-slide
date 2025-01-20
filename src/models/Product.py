class Product:
    def __init__(self,
                 sku: str,
                 images: list):
        self.sku = sku
        self.images = images

    def __str__(self):
        # for idx, img_link in enumerate(self.images, 1):
        #     print(f"{idx}. {img_link}")
        return f"\nProduct SKU: {self.sku} \nImages: {len(self.images)}"
