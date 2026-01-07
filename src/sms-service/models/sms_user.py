from pydantic import BaseModel, Field



"""
This pydantic model, is used for both validation of incoming and outgoing payloads.
"""
class SMSUser(BaseModel):
    user_id: str = Field(..., description="The unique identifier for the user, typically a UUID.", examples=["550e8400-e29b-41d4-a716-446655440000"])
    phone_number: str = Field(..., description="The unique phone number for the user.", examples=["09060540946"])
    country_code: str = Field(..., description="The country code, where the user number is located", examples=["+234", "+41", "+1"])
    is_active: bool = Field(..., default=True, description="Is the user still valid, or their number still valid")