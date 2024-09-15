from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, field_validator

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class NewEventModel(MongoBaseModel):
    eventName: str = Field(..., title="Event Name", description="The name of the event")
    selectedDates: List[datetime] = Field(..., title="Selected Dates", description="List of selected date and time in ISO format")
    timeUnit: str = Field(..., title="Time Unit", description="The unit of time (e.g., '1 hour')")
    earliestTime: str = Field(..., title="Earliest Time", description="The earliest time of the day (e.g., '08:00')")
    latestTime: str = Field(..., title="Latest Time", description="The latest time of the day (e.g., '22:00')")
    url: str = Field(..., title="URL", description="The unique URL of the event")
