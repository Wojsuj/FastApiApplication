from fastapi import FastAPI
from fastapi.responses import FileResponse
app = FastAPI()

image_url = "/images/800x400"

@app.get("/")
async def read_image(item_id: int):
    return FileResponse(image_url)