from pydantic import BaseModel


class ImageBase(BaseModel):
    path: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True