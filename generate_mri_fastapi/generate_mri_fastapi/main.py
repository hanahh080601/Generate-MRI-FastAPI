from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.image import image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
    # "http://localhost:3000",
    # "http://127.0.0.1:3000",
    # "http://192.168.0.12:3000",
    # "http://192.168.0.13:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(image)
