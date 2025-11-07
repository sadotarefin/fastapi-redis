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

def get_redis_data(key: str):
    try:
        cached_item = redis_client.get(key)
        if cached_item:
            return cached_item
    except Exception as e:
        print("Exception happend while loading data from cache {e}")
    return None

def set_redis_data(key: str, data: str, expire_seconds: int = 3600):
    try:
        redis_client.set(key, data, ex=expire_seconds)
    except Exception as e:
        print("Exception happened while writing data to cache {e}")

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    key = f"item_{item_id}"
    cached_item = get_redis_data(key)
    
    if cached_item:
        return {"item_id": item_id, "cached": True, "data": cached_item} 
    
    item = str.format("This is a item description with item id {}", item_id)
    
    set_redis_data(key, item) #save data to redis (if redis is available)
    
    return {"item_id": item_id, "cached": False, "data": item} 