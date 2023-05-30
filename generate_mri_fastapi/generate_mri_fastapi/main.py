from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.image import image

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(image)