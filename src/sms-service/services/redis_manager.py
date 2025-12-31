"""
This module manages the Redis connection for the SMS service.
It establishes a connection pool to the Redis server using the provided REDIS_URL.
"""
from typing import Dict
from lifespan import bootup_redis
from redis import asyncio as aioredis


"""
This async function serves the purpose of returning a connection
from the redis pool, this in turn is used for further Redis operaions
"""
async def get_redis_connection():
    redis_pool = await bootup_redis()
    print("Redis pool in get_redis_conn: ", redis_pool)
    redis_connection = await aioredis.Redis(connection_pool=redis_pool)
    print(f"Redis connection {redis_connection}")
    return redis_connection



"""
This async function serves the purpose of returning a user from the redis store
or passing it over to the DB
"""
async def get_user_by_id(user_id: str) -> Dict:
    pass



"""
This function serves the purpose of commiting a new entry to redis store
"""
async def commit_user(payload: Dict) -> bool:
    pass