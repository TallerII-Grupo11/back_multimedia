import os
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SongModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    artist: str = Field(...)
    album: str = Field(...)
    duration_seconds: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Cancion Animal",
                "artist": "Soda Stereo",
                "album": "Cancion Animal",
                "duration_seconds": "120.0",
            }
        }


class UpdateSongModel(BaseModel):
    name: Optional[str]
    artist: Optional[str]
    album: Optional[str]
    duration_seconds: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Cancion Animal",
                "artist": "Soda Stereo",
                "album": "Cancion Animal",
                "duration_seconds": "120.0",
            }
        }