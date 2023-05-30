from models.image import Image
from pymongo import MongoClient
from config.mongodb import Settings

settings = Settings()
conn = MongoClient(settings.DB_CONNECTION_STRING)

# async def add_2d_image(file: UploadFile = File(...), contrast: str = 't1') -> Comment:
#     contents = await file.read()
#     img = Image.open(io.BytesIO(contents))

#     image_dict = {
#         'filename': img,
#         'contrast': contrast
#     }
#     predict = Image.parse_obj(comment_dict)
#     conn.hanlhn.comments.insert_one(dict(predict))