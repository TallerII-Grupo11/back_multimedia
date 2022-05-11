from app.db.model.py_object_id import PyObjectId
from pydantic import Field

from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId


class SongModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    artists: List[str] = Field(...)
    album_id: str = None
    description: str = Field(...)
    song_file: str = Field(...)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "artists": ["Soda Stereo"],
                "album_id": "album_id",
                "description": "Song",
                "song_file": "file_name"
            }
        }


class UpdateSongModel(BaseModel):
    title: Optional[str]
    artists: Optional[List[str]]
    album_id: Optional[str]
    description: Optional[str]
    song_file: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "artists": ["Soda Stereo"],
                "album_id": "album_id",
                "description": "Song",
                "song_file": "file_name"
            }
        }
