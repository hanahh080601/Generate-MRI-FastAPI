def commentEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "comment": str(item["comment"]),
        "sentiment": str(item["sentiment"])
    }

def commentEntities(entity) -> list:
    return [commentEntity(item) for item in entity]