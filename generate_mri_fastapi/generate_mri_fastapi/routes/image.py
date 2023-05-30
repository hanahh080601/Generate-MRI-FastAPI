from fastapi import APIRouter
from database.database import conn
from schemas.image import imageEntity, imageEntities
from generator import generator
from fastapi import File, UploadFile
from PIL import Image
import io

image = APIRouter()

@image.get('/')
async def list_all_comments():
    return imageEntities(conn.hanlhn.mri_image.find())

@image.post('/')
async def generate_image(file: UploadFile = File(...), contrast: str = 't1'):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        pred = generator.generate(img, contrast)
    except Exception as e:
        print(e)
    return pred