def imageEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "filename": str(item["filename"]),
        "dataset": str(item["dataset"]),
        "contrast": str(item["contrast"])
    }

def imageEntities(entity) -> list:
    return [imageEntity(item) for item in entity]