from src.common.utils import read_excel_data


def main():
    excel_file = "data/product-images.xlsx"
    objects = read_excel_data(excel_file)


if __name__ == '__main__':
    main()
