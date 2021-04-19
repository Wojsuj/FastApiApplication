from app import models, crud
import random
import cv2
import numpy as np
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import shutil
import os

def get_thumbnail_size(size: str) -> tuple:

    try: width, height = size.split("x")
    except ValueError:
        raise HTTPException(status_code=418,
                            detail="You cannot pass value in this format! The proper format is {width}x{height}!")
    if not width.isnumeric(): raise HTTPException(status_code=419,
                            detail="You cannot pass value in this format! Width has to be a number!")
    if not height.isnumeric(): raise HTTPException(status_code=419,
                            detail="You cannot pass value in this format! Height has to be a number!")
    return int(width), int(height)

def get_random_id(db: Session, item : models) -> int:

    items_amount = len(db.query(item).all())
    if items_amount == 0:  raise HTTPException(status_code=404,
                            detail="Error 404! No items in database!")
    random_id = random.randint(1, items_amount)
    return random_id

def read_image(image_path:str) -> np.ndarray:
    if type(image_path) is not str: raise HTTPException(status_code=419,
                            detail="Path to image has to be in a string format!")
    return cv2.imread(filename= image_path)

def resize_image(image: np.ndarray, resize_width: int, resize_height:int) -> np.ndarray:
    image_width, image_height = get_image_size(image = image)

    if resize_width > image_width or resize_height > image_height: raise HTTPException(status_code=419,
                            detail="Cannot enlarge image!")
    return cv2.resize(src  = image, dsize = (int(resize_width), int(resize_height)))

def change_image_to_png_format(image: np.ndarray) -> np.ndarray:
    res, png_image = cv2.imencode(ext = ".png", img = image)
    return png_image

def load_random_image(db:Session , size: str) -> tuple:
    width, height = get_thumbnail_size(size = size)
    random_id = get_random_id(db = db, item = models.Image)
    db_image_path = crud.get_image(db = db, image_id=random_id).path
    print(db_image_path)
    image = read_image(db_image_path)

    resized_image = resize_image(image = image, resize_width = width, resize_height= height)
    png_image = change_image_to_png_format(image = resized_image)
    return db_image_path, png_image

def load_image_at_given_path(size: str, image_path: str) -> np.ndarray:
    width, height = get_thumbnail_size(size = size)
    image = read_image(image_path = image_path)
    resized_image = resize_image(image = image, resize_width = width, resize_height= height)
    png_image = change_image_to_png_format(image = resized_image)
    return png_image

def get_image_size(image: np.ndarray) -> tuple:
    height, width, channels = image.shape
    return width, height

def save_image_to_disk(image: UploadFile):
    path = f"images/"
    if not os.path.exists(path): os.mkdir(path)
    with open(os.path.join(path, image.filename), "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
