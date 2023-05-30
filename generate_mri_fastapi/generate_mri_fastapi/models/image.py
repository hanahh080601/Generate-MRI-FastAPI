from pydantic import BaseModel

class Image(BaseModel):
    filename: str 
    dataset: str
    contrast: str