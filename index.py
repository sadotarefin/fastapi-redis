from fastapi import FastAPI
import redis

app = FastAPI()

from redis import ConnectionPool, Redis

POOL_SIZE = 50 #recommended for small setup
TIMEOUT_SECONDS = .05 #recommended 10 times than redis response time.    

pool = ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=POOL_SIZE,
    socket_timeout=TIMEOUT_SECONDS
)
redis_client = Redis(connection_pool=pool)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    try:
        cached_item = redis_client.get(f"item_{item_id}")
        if cached_item:
            return {"item_id": item_id, "cached": True, "data": cached_item} 
    except Exception as e:
        print("Exception happened while loading data from cache {e}")
        pass
    item = str.format("This is a item description with item id {}", item_id)
    try:
        redis_client.set(f"item_{item_id}", item)
    except Exception as e:
        print("Exception happened while writing data to cache {e}")
        pass
    return {"item_id": item_id, "cached": False, "data": item} 