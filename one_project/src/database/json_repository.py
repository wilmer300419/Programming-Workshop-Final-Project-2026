import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "products.json")


def read_products():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def write_products(products):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            products,
            file,
            indent=4,
            ensure_ascii=False
        )