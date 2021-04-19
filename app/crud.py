from sqlalchemy.orm import Session

from . import models, schemas


def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Image).offset(skip).limit(limit).all()

def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def get_image_by_path(db: Session, path: str):
    return db.query(models.Image).filter(models.Image.path == path).first()

def create_image(db: Session, image_path: str):

    db_image = models.Image(path = image_path)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
