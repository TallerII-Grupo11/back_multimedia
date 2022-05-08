from abc import abstractmethod
from typing import List

from app.db.model.song import SongModel, UpdateSongModel
from app.db.model.album import AlbumModel, UpdateAlbumModel, AlbumSongModel


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

    # --- Songs ---
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

    @abstractmethod
    async def list_songs_in_album(self, album_id: str) -> List[UpdateSongModel]:
        pass

    # --- Albums ---
    @abstractmethod
    async def get_albums(self) -> List[UpdateAlbumModel]:
        pass

    @abstractmethod
    async def get_album(self, album_id: str) -> AlbumSongModel:
        pass

    @abstractmethod
    async def add_album(self, album: AlbumModel):
        pass

    @abstractmethod
    async def update_album(self, album_id: str, album: UpdateAlbumModel):
        pass

    @abstractmethod
    async def delete_album(self, album_id: str):
        pass

    @abstractmethod
    async def get_albums_by_artist(self, artist: str) -> List[AlbumSongModel]:
        pass

    @abstractmethod
    async def get_albums_by_subscription(
        self, 
        subscription: str
    ) -> List[UpdateAlbumModel]:
        pass
