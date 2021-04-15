from sql_app import models
import random
import cv2
def get_image_size(size: str) -> tuple:
    width, height = size.split("x")
    return int(width), int(height)

def get_random_id(db, item) -> int:
    items_amount = len(db.query(item).all())
    random_id = random.randrange(start=0, stop=items_amount)
    return random_id

def read_image(image_name):
    return cv2.imread(f"images/{image_name}.jpg")

def resize_image(image, width, height):
    return cv2.resize(image, (int(width), int(height)))

def change_to_png(image):
    res, png_image = cv2.imencode(".png", image)
    return png_image
