from abc import abstractmethod
from typing import List

from app.db.models import SongModel, UpdateSongModel
from fastapi import Body



class DatabaseManager(object):
    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    @abstractmethod
    async def connect_to_database(self, path: str):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def get_songs(self) -> List[UpdateSongModel]:
        pass

    @abstractmethod
    async def get_song(self, song_id: str) -> SongModel:
        pass

    @abstractmethod
    async def add_song(self, song: SongModel):
        pass

    @abstractmethod
    async def update_song(self, song_id: str, song: UpdateSongModel):
        pass

    @abstractmethod
    async def delete_song(self, song_id: str):
        pass
