from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi import FastAPI, File, UploadFile
import io
from starlette.responses import StreamingResponse
from functional_module import helper_functions
from pymemcache.client import base


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
async def upload_image(image: UploadFile = File(...), db: Session = Depends(get_db)):
    path = f"images/{image.filename}"
    image_path = crud.get_image_by_path(db = db, path=path)
    if image_path is not None:
        raise HTTPException(status_code=500, detail="Image already exist in database!")
    helper_functions.save_image_to_disk(image = image)
    crud.create_image(db=db, image_path = path)
    return {"filename": image.filename}


@app.get("/images/{size}", response_model=List[schemas.Image])
async def create_thumbnail(size: str , db: Session = Depends(get_db)):

    cached_image_path = cache.get(key = size)

    if cached_image_path is not None:
        cached_image_path = cached_image_path.decode('utf-8')
        cached_image = helper_functions.load_image_at_given_path(size = size, image_path=cached_image_path)
        return StreamingResponse(io.BytesIO(cached_image.tobytes()), media_type="image/png")

    else:
        image_path, random_image = helper_functions.load_random_image(db = db, size = size)
        cached_image_path = image_path
        cache.set(key = size, value = cached_image_path, expire = 60*60)

    return StreamingResponse(io.BytesIO(random_image.tobytes()), media_type="image/png")