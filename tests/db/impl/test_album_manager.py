import unittest
from unittest.mock import MagicMock

from app.db.impl.album_manager import AlbumManager
from app.db.model.album import AlbumModel
from app.db.model.artist import ArtistModel


def get_album_mock() -> AlbumModel:
    return AlbumModel(
        id="62be27922d98b5aaad951f95",
        title="title",
        artist=ArtistModel(artist_id="id", artist_name="name"),
        description="description",
        genre="genre",
        subscription="free",
        image="image",
    )


class TestAlbumManager(unittest.TestCase):
    db = MagicMock()

    async def test_get_albums(self):
        album = get_album_mock()
        self.db["albums"].find = MagicMock(return_value=[album])
        album_manager = AlbumManager(self.db)
        result = await album_manager.get_albums()

        assert len(result) == 1

    async def test_get_album(self):
        album = get_album_mock()
        self.db["albums"].find_one = MagicMock(return_value=album)
        album_manager = AlbumManager(self.db)
        result = await album_manager.get_album("id")

        assert result is not None

    async def test_get_albums_by_artist(self):
        album = get_album_mock()
        self.db["albums"].find = MagicMock(return_value=[album])
        album_manager = AlbumManager(self.db)
        result = await album_manager.get_albums_by_artist("artist_name")

        assert len(result) == 1

    async def test_get_albums_by_subscription(self):
        album = get_album_mock()
        self.db["albums"].find = MagicMock(return_value=[album])
        album_manager = AlbumManager(self.db)
        result = await album_manager.get_albums_by_subscription("premium")

        assert len(result) == 1

    async def test_get_albums_by_genre(self):
        album = get_album_mock()
        self.db["albums"].find = MagicMock(return_value=[album])
        album_manager = AlbumManager(self.db)
        result = await album_manager.get_albums_by_genre("rock")

        assert len(result) == 1

    async def test_get_albums_by_song(self):
        album = get_album_mock()
        self.db["albums"].find_one = MagicMock(return_value=album)
        album_manager = AlbumManager(self.db)
        result = await album_manager.get_albums_by_song("id")

        assert result is not None
