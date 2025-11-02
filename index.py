from fastapi import FastAPI
import redis

app = FastAPI()

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    cached_item = redis_client.get(f"item_{item_id}")
    if cached_item:
        return {"item_id": item_id, "item": cached_item}
    item = str.format("This is a item description with item id {}", item_id)
    redis_client.set(f"item_{item_id}", item)
    return {"item_id": item_id, "item": item}