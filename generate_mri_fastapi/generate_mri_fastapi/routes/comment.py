from fastapi import APIRouter
from database.database import conn, add_comment
from schemas.comment import commentEntity, commentEntities
from predict import prediction

comment = APIRouter()

@comment.get('/')
async def list_all_comments():
    return commentEntities(conn.hanlhn.comments.find())

@comment.post('/')
async def predict_sentiment(comment: str):
    try:
        pred = prediction.predict(comment)
        await add_comment(comment, pred)
    except Exception as e:
        print(e)
    return pred