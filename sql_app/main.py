from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi import FastAPI, File, UploadFile
import io
from starlette.responses import StreamingResponse
from Scripts import helper_functions

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
    if not (len(db.query(models.Image).all())): raise HTTPException(status_code=404, detail="404 Error!")
    width, height = helper_functions.get_image_size(size)
    random_id = helper_functions.get_random_id(db, models.Image)
    db_image_name = crud.get_image(db, image_id=random_id).name
    image = helper_functions.read_image(db_image_name)
    resized_image = helper_functions.resize_image(image, width, height)
    png_image = helper_functions.change_to_png(resized_image)

    return StreamingResponse(io.BytesIO(png_image.tobytes()), media_type="image/png")