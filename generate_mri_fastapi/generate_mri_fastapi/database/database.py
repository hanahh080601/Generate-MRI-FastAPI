from models.comment import Comment
from pymongo import MongoClient
from config.mongodb import Settings

settings = Settings()
conn = MongoClient(settings.DB_CONNECTION_STRING)

async def add_comment(comment: str, pred_msg: str) -> Comment:
    comment_dict = {
        'comment': comment,
        'sentiment': pred_msg
    }
    predict = Comment.parse_obj(comment_dict)
    conn.hanlhn.comments.insert_one(dict(predict))