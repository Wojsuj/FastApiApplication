from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi import FastAPI, File, UploadFile
import io
from starlette.responses import StreamingResponse
from Scripts import helper_functions
from pymemcache.client import base
import shutil
from fastapi.responses import JSONResponse
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

cache = base.Client(('localhost', 11211))


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/images/")
async def image(image: UploadFile = File(...), db: Session = Depends(get_db)):
    path = f"images/{image.filename}"
    image_path = crud.get_image_by_path(db, path=path)
    if image_path is not None:
        raise HTTPException(status_code=500, detail="Image already exist in database!")

    with open(f"images/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    crud.create_image(db=db, image_path = path)
    return {"filename": image.filename}


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
async def create_thumbnail(size: str , db: Session = Depends(get_db)):
    images_amount = helper_functions.items_amount(db, models.Image)
    if images_amount == 0: raise HTTPException(status_code=404, detail="404 Error!")

    cached_image_name = cache.get(size)

    if cached_image_name is not None:
        cached_image_name = cached_image_name.decode('utf-8')
        cached_image = helper_functions.get_image(size, cached_image_name)
        return StreamingResponse(io.BytesIO(cached_image.tobytes()), media_type="image/png")

    else:
        image_name, random_image = helper_functions.get_random_image(db, size)
        cached_image_name = image_name
        cache.set(size, cached_image_name, 5)

    return StreamingResponse(io.BytesIO(random_image.tobytes()), media_type="image/png")