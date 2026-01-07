import pytest
import asyncio
from sqlalchemy import text
from utils.db_engine import get_engine as get_async_engine

@pytest.fixture(scope="session")
def event_loop():
    """Override the main event loop to ensure a long lived loop, for the entire session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine():
    _engine = await get_async_engine()
    yield _engine
    await _engine.dispose()



@pytest.fixture(autouse=True)
async def db_cleanup():
    """Ensure the database is clean before each test"""
    yield

    # Yiled allows the test to run first, then cleanup happens after
    engine = await get_async_engine()
    async with engine.connect() as conn:
        # Use TRUNCATE for high-speed erasure
        await conn.execute(text("TRUNCATE TABLE sms_users RESTART IDENTITY CASCADE;"))
        await conn.commit()