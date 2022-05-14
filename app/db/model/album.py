from app.db.model.py_object_id import PyObjectId
from pydantic import Field

from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId
from app.db.model.song import SongModel
from app.db.model.subscription import Subscription


class AlbumModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    artist: str = Field(...)
    description: str = Field(...)
    genre: str = Field(...)
    images: List[str] = Field(...)
    subscription: Subscription = Field(...)
    songs: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, Subscription: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "artist": "Soda Stereo",
                "description": "Song",
                "genre": "rock",
                "images": ["image.png"],
                "subscription": "free",
                "songs": []
            }
        }


class UpdateAlbumModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    artist: Optional[str]
    genre: Optional[str]
    images: Optional[List[str]]
    subscription: Optional[Subscription]
    songs: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, Subscription: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "artist": "Soda Stereo",
                "description": "Song",
                "genre": "rock",
                "images": ["image.png"],
                "subscription": "free",
                "songs": []
            }
        }


class SongAlbumModel(BaseModel):
    songs: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, Subscription: str}
        schema_extra = {
            "example": {
                "songs": []
            }
        }
