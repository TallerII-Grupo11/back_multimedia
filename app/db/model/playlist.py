from app.db.model.py_object_id import PyObjectId
from pydantic import Field

from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId
from app.db.model.song import SongModel


class PlaylistModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    description: str = Field(...)
    songs: List[str] = []
    is_collaborative: str = Field(...)
    owner_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "description": "Song",
                "songs": [],
                "is_collaborative": "no",
                "owner_id": "user_id"
            }
        }


class UpdatePlaylistModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    songs: Optional[List[str]]
    is_collaborative: Optional[str]
    owner_id: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "description": "Song",
                "songs": [],
                "is_collaborative": "no",
                "owner_id": "user_id"
            }
        }


class SongPlaylistModel(BaseModel):
    songs: Optional[List[str]]
    owner_id: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "songs": [],
                "owner_id": "user_id"
            }
        }
