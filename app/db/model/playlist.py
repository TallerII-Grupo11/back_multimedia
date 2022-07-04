from app.db.model.py_object_id import PyObjectId
from pydantic import Field

from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId


class PlaylistModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    description: str = Field(...)
    songs: List[str] = []
    is_collaborative: bool = Field(...)
    owner_id: str = Field(...)

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "description": "Song",
                "songs": ["song_id_1", "song_id_2"],
                "is_collaborative": False,
                "owner_id": "user_id"
            }
        }


class UpdatePlaylistModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    songs: Optional[List[str]]
    is_collaborative: Optional[bool]
    owner_id: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "description": "Song",
                "songs": ["song_id_1", "song_id_2"],
                "is_collaborative": False,
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
                "songs": ["song_id_1", "song_id_2"],
                "owner_id": "user_id"
            }
        }
