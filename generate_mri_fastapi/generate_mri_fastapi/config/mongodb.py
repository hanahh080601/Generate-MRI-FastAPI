from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_CONNECTION_STRING: str = "mongodb+srv://hana:1234@cluster0.7awqr.mongodb.net/hanlhn?authSource=admin&replicaSet=atlas-c0jjq4-shard-0&readPreference=primary&ssl=true"
