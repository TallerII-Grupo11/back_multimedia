from app.db.model.py_object_id import PyObjectId
from pydantic import Field

from pydantic.main import BaseModel
from pydantic import validator
from typing import List, Optional
from bson import ObjectId
from app.db.model.subscription import Subscription
from app.db.model.artist import ArtistModel


class AlbumModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    artist: ArtistModel = Field(...)
    description: str = Field(...)
    genre: str = Field(...)
    image: str = Field(...)
    subscription: str = Field(...)
    songs: List[str] = []

    @validator('subscription')
    def subscription_values(cls, v):
        if v not in ["free", "normal", "premium"]:
            raise ValueError(f'Subscription value {v} not allowed')
        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, Subscription: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "artist": {
                    "artist_id": "artist_id",
                    "artist_name": "Soda Stereo",
                },
                "description": "Song",
                "genre": "rock",
                "image": "image.png",
                "subscription": "free",
                "songs": ["song_id_1", "song_id_2"]
            }
        }


class UpdateAlbumModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    artist: Optional[ArtistModel]
    genre: Optional[str]
    image: Optional[str]
    subscription: Optional[Subscription]
    songs: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, Subscription: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "artist": {
                    "artist_id": "artist_id",
                    "artist_name": "name",
                },
                "description": "Song",
                "genre": "rock",
                "image": "image.png",
                "subscription": "free",
                "songs": ["song_id_1", "song_id_2"]
            }
        }


class SongAlbumModel(BaseModel):
    songs: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "songs": ["song_id_1", "song_id_2"]
            }
        }
