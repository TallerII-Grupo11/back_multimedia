import unittest
from unittest.mock import MagicMock

from app.db.impl.song_manager import SongManager
from app.db.model.song import SongModel
from app.db.model.artist import ArtistModel


def get_song_mock() -> SongModel:
    return SongModel(
        id="62be27922d98b5aaad951f95",
        title="title",
        artists=[ArtistModel(artist_id="id", artist_name="name")],
        description="description",
        genre="genre",
        song_file="file",
    )


class TestSongManager(unittest.TestCase):
    db = MagicMock()

    async def test_get_all_songs(self):
        song1 = get_song_mock()
        song2 = get_song_mock()
        self.db["songs"].find = MagicMock(return_value=[song1, song2])
        song_manager = SongManager(self.db)
        result = await song_manager.get_all_songs()

        assert len(result) == 2

    async def test_get_song(self):
        song = get_song_mock()
        self.db["songs"].find_one = MagicMock(return_value=song)
        song_manager = SongManager(self.db)
        result = await song_manager.get_song("id")

        assert result is not None

    async def test_delete_song(self):
        self.db["songs"].delete_one = MagicMock(return_value=True)
        song_manager = SongManager(self.db)
        result = await song_manager.delete_song("id")

        assert result

    async def test_list_songs_by_artist(self):
        song = get_song_mock()
        self.db["songs"].find = MagicMock(return_value=[song])
        song_manager = SongManager(self.db)
        result = await song_manager.list_songs_by_artist("artist_name")

        assert len(result) == 1

    async def test_list_songs_by_genre(self):
        song = get_song_mock()
        self.db["songs"].find = MagicMock(return_value=[song])
        song_manager = SongManager(self.db)
        result = await song_manager.list_songs_by_genre("rock")

        assert len(result) == 1

    async def test_get_songs_with_query(self):
        song = get_song_mock()
        self.db["songs"].find = MagicMock(return_value=[song])
        song_manager = SongManager(self.db)
        result = await song_manager.get_songs("query")

        assert len(result) == 1
