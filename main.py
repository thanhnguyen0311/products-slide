from src.Enum.FilePath import FilePath
from src.common.utils import read_excel_data
from src.common.editor import create_slide


def main():
    excel_file = "data/product-images.xlsx"
    products = read_excel_data(excel_file)
    for product in products:
        create_slide(product)


if __name__ == '__main__':
    main()