from lifespan import app, get_db_engine
from services.redis_manager import get_redis_connection
from services.rabbit_manager import get_rabbitmq_connection



@app.get("/health")
async def system_health_check():
    redis_conn = await get_redis_connection()
    rabbit_conn = await get_rabbitmq_connection()
    print("Rabbit_conn:",rabbit_conn)
    print("Redis_conn:",redis_conn)
    return {"status": "ok", "redis_con": str(redis_conn), "rabbit_con": str(rabbit_conn)}

@app.get("/db-engine")
async def db_engine_check():
    db_engine = await get_db_engine()
    print("DB Engine:", db_engine)
    return {"db_engine": str(db_engine)}