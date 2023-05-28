from fastapi import FastAPI
from routes.comment import comment

app = FastAPI()
app.include_router(comment)