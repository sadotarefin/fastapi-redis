from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = str.format("This is a item description with item id {}", item_id)
    return {"item_id": item_id, "item": item}

