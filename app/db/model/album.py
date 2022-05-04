from app.db.model.py_object_id import PyObjectId
from pydantic import Field
from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId
from app.db.model.song import SongModel


class AlbumModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    description: str = Field(...)
    genre: str = Field(...)
    images: List[str] = Field(...)
    suscriptions: List[str] = Field(...)
    songs: List[SongModel] = Field(...)


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "description": "Song",
                "genre": "rock",
                "images": ["image.png"],
                "suscriptions": ["s1", "s2"],
                "songs": [
                    {
                        "title": "Musica Ligera",
                        "artists": ["Soda Stereo"],
                        "album": "Cancion Animal",
                        "description": "Song",
                        "file": "file_name"
                    }
                ]
            }
        }


class UpdateAlbumModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    genre: Optional[str]
    images: Optional[List[str]]
    suscriptions: Optional[List[str]]
    songs: Optional[List[SongModel]]


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "description": "Song",
                "genre": "rock",
                "images": ["image.png"],
                "suscriptions": ["s1", "s2"],
                "songs": [
                    {
                        "title": "Musica Ligera",
                        "artists": ["Soda Stereo"],
                        "album": "Cancion Animal",
                        "description": "Song",
                        "file": "file_name"
                    }
                ]
            }
        }
