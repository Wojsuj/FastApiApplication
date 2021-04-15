from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

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
    return crud.create_image(db=db)


@app.get("/images/", response_model=List[schemas.Image])
def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = crud.get_images(db, skip=skip, limit=limit)
    return images


@app.get("/images/{image_id}", response_model=schemas.Image)
def read_user(image_id: int, db: Session = Depends(get_db)):
    db_image  = crud.get_image(db, image_id=image_id)
    if db_image  is None:
        raise HTTPException(status_code=404, detail="Image not found!")
    return db_image

