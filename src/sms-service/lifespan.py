from contextlib import asynccontextmanager
from fastapi import FastAPI

from redis import asyncio as aioredis
import aio_pika
import aio_pika.abc
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from dotenv import load_dotenv
import os, sys
import logging


load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", stream=sys.stdout)
logger = logging.getLogger(__name__)


REDIS_URL = os.getenv("REDIS_URL")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
POSTGRESQL_URL = os.getenv("DATABASE_URL")



if REDIS_URL is None:
    raise "Redis URL is None"

if RABBITMQ_URL is None:
    raise "RabbitMQ URL is None"


if POSTGRESQL_URL is None:
    raise "PostgreSQL URL is None"



"""
This following functions handles the bootup process for connecting to Redis, RabbitMQ, and PostgreSQL.
It attempts to establish connections to each service and logs the success or failure of each connection attempt.
"""
async def bootup_redis():
     # An attempt to connect to the Redis Server: Async
    logger.info("Attempt to connect to Redis Server")
    try:
        redis_pool = aioredis.ConnectionPool.from_url(REDIS_URL,decode_responses=True,max_connections=20)
        logger.info(f"Redis connection success: {redis_pool}")
        return redis_pool
    except Exception as redis_conn_error:
        logger.error(f"Could not connect to Redis: {redis_conn_error}")
        raise


async def bootup_rabbitmq():
    # An attempt to connect to the RabbitMQ server: Async
    logger.info("Attempt to connect to RabbitMQ Server")
    try:
        rabbitmq_connection: aio_pika.abc.AbstractRobustConnection = await aio_pika.connect_robust(RABBITMQ_URL)
        logger.info(f"RabbitMQ connection success: {rabbitmq_connection}")
        return rabbitmq_connection
    except Exception as rabbitmq_conn_error:
        logger.error(f"Could not connect to RabbitMQ: {rabbitmq_conn_error}")
        raise



async def bootup_postgresql():
    # An attempt to connect to the PostgreSQL server: Async
    logger.info("Attempt to connect to PostgreSQL Server")
    try:
        engine = create_async_engine(POSTGRESQL_URL, echo=True)
        async_session = async_sessionmaker(engine, expire_on_commit=False)
        # Test connection
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: None)  # Simple no-op to test connection
        logger.info(f"PostgreSQL connection success: {engine}")
        return async_session
    except Exception as postgresql_conn_error:
        logger.error(f"Could not connect to PostgreSQL: {postgresql_conn_error}")
        raise
    pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Preflight checks.....")

    # Connection attempts
    reddit_pool = await bootup_redis()
    rabbitmq_connection = await bootup_rabbitmq()
    postgresql_connection = await bootup_postgresql()

    yield

    # Cleanup code pre server shutdown
    logger.info("Shutting down connections.....")
    await reddit_pool.disconnect() 
    await rabbitmq_connection.close()
    await postgresql_connection.close_all()


app = FastAPI(title="sms-servive", lifespan=lifespan)

