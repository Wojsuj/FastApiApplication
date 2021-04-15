from sql_app import models, crud
import random
import cv2
def get_image_size(size: str) -> tuple:
    width, height = size.split("x")
    return int(width), int(height)

def get_random_id(db, item) -> int:
    items_amount = len(db.query(item).all())

    random_id = random.randint(1, items_amount)
    print(random_id)
    return random_id

def read_image(image_name):
    return cv2.imread(f"images/{image_name}.jpg")

def resize_image(image, width, height):

    return cv2.resize(image, (int(width), int(height)))

def change_to_png(image):
    res, png_image = cv2.imencode(".png", image)
    return png_image


def get_random_image(db, size):
    width, height = get_image_size(size)
    random_id = get_random_id(db, models.Image)
    db_image_name = crud.get_image(db, image_id=random_id).name

    image = read_image(db_image_name)
    resized_image = resize_image(image, width, height)
    png_image = change_to_png(resized_image)
    return db_image_name, png_image

def get_image(size, image_name):


    width, height = get_image_size(size)

    image = read_image(image_name)
    resized_image = resize_image(image, width, height)
    png_image = change_to_png(resized_image)
    return png_image



