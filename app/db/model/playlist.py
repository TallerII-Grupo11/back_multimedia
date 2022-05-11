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
    user_owner: str = Field(...)

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
                "user_owner": "user_id"
            }
        }


class UpdatePlaylistModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    songs: Optional[List[str]]
    is_collaborative: Optional[str]
    user_id: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "description": "Song",
                "songs": [],
                "is_collaborative": "no",
                "user_id": "user_id"
            }
        }


class PlaylistSongModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    songs: Optional[List[SongModel]]
    is_collaborative: Optional[str]
    user_owner: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "description": "Song",
                "songs": [],
                "is_collaborative": "no",
                "user_owner": "user_id"
            }
        }
