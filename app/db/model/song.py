from app.db.model.py_object_id import PyObjectId
from pydantic import Field

from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId
from app.db.model.artist import ArtistModel


class SongModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    artists: List[ArtistModel] = Field(...)
    description: str = Field(...)
    genre: str = Field(...)
    song_file: str = Field(...)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "artists": [
                    {
                        "artist_id": "id",
                        "artist_name": "name",
                    }
                ],
                "description": "Song",
                "song_file": "file_name",
                "genre": "genre_name",
            }
        }


class UpdateSongModel(BaseModel):
    title: Optional[str]
    artists: Optional[List[ArtistModel]]
    description: Optional[str]
    song_file: Optional[str]
    genre: Optional[str]

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Cancion Animal",
                "artists": [
                    {
                        "artist_id": "id",
                        "artist_name": "name",
                    }
                ],
                "description": "Song",
                "song_file": "file_name",
                "genre": "genre_name",
            }
        }
