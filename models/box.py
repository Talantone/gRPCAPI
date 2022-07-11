import datetime
from typing import Optional, Any

from beanie import Document, PydanticObjectId
from pydantic import BaseModel

class Box(Document):

    class Settings:
        name = "boxes"

    name: str
    id: Optional[int] = None
    price: int
    description: str
    category: str
    quantity: int
    created_at: datetime.datetime

    class Config:
        schema_extra = {
            "example": {
                "name": "OrangeBox",
                "price": 60,
                "description": "Valve games collection",
                "category": "games",
                "quantity": 100000,
            }
        }

class UpdateBoxModel(BaseModel):
    name: Optional[str]
    price: Optional[int]
    description: Optional[str]
    category: Optional[str]
    quantity: Optional[int]

    class Collection:
        name = "box"

    class Config:
        schema_extra = {
            "example": {
                "name": "OrangeBox",
                "price": 60,
                "description": "Valve games collection",
                "category": "games",
                "quantity": 100000,
            }
        }

class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data"
            }
        }

