import pytest
from uuid import uuid4
from datetime import datetime, timezone
from services.postgresql_manager import find_user_by, create_user, delete_user
from models.sms_user import SMSUser



@pytest.mark.asyncio
async def test_complete_lifecycle(engine):
    # 1. Setup the Identity
    test_id = uuid4()
    test_phone = "+2340000000000"
    
    payload = {
        "user_id": str(test_id),
        "phone_number": test_phone,
        "country_code": "NG",
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }

    # A Pydantic check
    pydantic_dict = SMSUser(**payload).model_dump(mode="json")
    print(f"Pydantic validation successful: {pydantic_dict}")
    # # 2. Test Persistence  (CREATE)
    # created = await create_user(payload)