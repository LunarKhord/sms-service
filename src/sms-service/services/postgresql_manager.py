"""
This module serves the purpose of managing PostgreSQL connections for the SMS service.
It handles the CRUD operations related to user data within the PostgreSQL database.
"""
from uuid import UUID
from typing import Dict, Any, Optional
from sqlalchemy import text
from lifespan import get_db_engine
import logging
from models.sms_user import SMSUser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def find_user_by[T](identifier: T) -> Dict[str, Any] | None:
    """
    A Generic seeker that hunts for a user by either their 
    Sovereign ID (UUID) or their Physical Address (Phone Number).
    """
    search_query = text("""
        SELECT user_id, phone_number, is_active, country_code 
        FROM sms_users 
        WHERE user_id::text = :val OR phone_number = :val
        LIMIT 1
    """)
    
    # Retrieve the Engine from the Lifespan Reservoir
    db_engine = await get_db_engine()
    try:
        async with db_engine.connect() as conn:
            # The 'Handshake' between the identifier and the :val placeholder
            result = await conn.execute(search_query, {"val": str(identifier)})
            logger.info(f"Attempte to find user by identifier: {identifier}")
            row = result.mappings().first()
            
        return dict(row) if row else None
    except Exception as e:
        logger.error("Error finding user by %s: %s", identifier, e)
        return None


"""
Commits a pre-validated user payload to the PostgreSQL ledger.
"""
async def create_user(payload: Dict[str, Any]) -> bool:
    # 1. The SQL 'Contract'
    # Note the reuse of :created_at for the updated_at column to ensure initial alignment.
    sql = text("""
        INSERT INTO sms_users (user_id, phone_number, country_code, is_active, created_at, updated_at) 
        VALUES (:user_id, :phone_number, :country_code, :is_active, :created_at, :updated_at)
    """)

    # 2. Acquisition of the Engine
    engine = await get_db_engine()

    try:
        async with engine.connect() as conn:
            # 3. Execution and Transaction Commitment
            await conn.execute(sql, payload)
            await conn.commit()
            
            logger.info(f"Sovereign User created successfully: {payload.get('user_id')}")
            return True

    except Exception as e:
        # CORRECTION: This is a Database/Persistence error, not a Pydantic one.
        logger.error(f"Catastrophic failure during Database Persistence: {e}")
        # In a production environment, you might re-raise the error or return False
        return False


"""
A Generic seeker that hunts for a user by either their 
Sovereign ID (UUID) or their Physical Address (Phone Number).
Delete an existing user's details in the PostgreSQL ledger.
"""
async def delete_user[T](identifier: T) -> bool:
    sql = text("""
        DELETE FROM sms_users 
        WHERE user_id::text = :val OR phone_number = :val
    """)
    
    engine = await get_db_engine()
    try:
        async with engine.connect() as conn:
            result = await conn.execute(sql, {"val": str(identifier)})
            await conn.commit()
            
            
            if result.rowcount > 0:
                logger.info(f"Successfully excised user: {identifier}")
                return True
                
            logger.warning(f"No user found for excision: {identifier}")
            return False
    except SQLAlchemyError as e:
        logger.error(f"Excision Failure for identifier {identifier}: {e}")
        return False