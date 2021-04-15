from sqlalchemy.orm import Session

from . import models, schemas


def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Image).offset(skip).limit(limit).all()

def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def get_image_by_name(db: Session, name: str):
    return db.query(models.Image).filter(models.Image.name == name).first()

def create_image(db: Session, item: schemas.ImageCreate, image_id: int):
    db_item = models.Image(**item.dict(), owner_id=image_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item