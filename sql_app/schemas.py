from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class ImageBase(BaseModel):
    path: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True