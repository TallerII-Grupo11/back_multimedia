import os

from bson import ObjectId
from pydantic import Field
from pydantic.main import BaseModel
from typing import List, Optional


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
    title: str = Field(...)
    artist: str = Field(...)
    album: str = Field(...)
    description: str = Field(...)


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Cancion Animal",
                "artist": "Soda Stereo",
                "album": "Cancion Animal",
                "description": "Song"
            }
        }


class UpdateSongModel(BaseModel):
    title: Optional[str]
    artist: Optional[str]
    album: Optional[str]
    description: Optional[str]


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "artist": "Soda Stereo",
                "album": "Cancion Animal",
                "description": "Song"
            }
        }
