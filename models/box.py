import datetime
from typing import Optional, Any

from google.protobuf.timestamp_pb2 import Timestamp
from beanie import Document, PydanticObjectId
from pydantic import BaseModel


class Time(BaseModel):
    nanos: int
    seconds: int


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

