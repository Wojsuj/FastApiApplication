from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi import FastAPI, File, UploadFile
import numpy as np
import base64
import cv2
import random
import uuid
import io
from starlette.responses import StreamingResponse
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/images/", response_model=schemas.Image)
def create_image(image: schemas.ImageCreate, db: Session = Depends(get_db)):
    db_image = crud.get_image_by_name(db, name = image.name)
    if db_image:
        raise HTTPException(status_code=400, detail="Image already exists!")
    return crud.create_image(db=db, image = image)


@app.get("/images/", response_model=List[schemas.Image])
def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = crud.get_images(db, skip=skip, limit=limit)
    return images


@app.get("/image_id/{image_id}", response_model=schemas.Image)
def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image  = crud.get_image(db, image_id=image_id)
    if db_image  is None:
        raise HTTPException(status_code=404, detail="Image not found!")
    return db_image

@app.get("/images/{size}", response_model=List[schemas.Image])
def create_thumbnail(size: str , db: Session = Depends(get_db)):
    width, height = size.split("x")

    number_images = len(db.query(models.Image).all())
    random_id = random.randrange(start = 0, stop = number_images)

    db_image_name = crud.get_image(db, image_id=random_id).name

    cv2img = cv2.imread(f"images/{db_image_name}.JPG")
    cv2img = cv2.resize(cv2img, (int(width), int(height)))
    res, im_png = cv2.imencode(".png", cv2img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")