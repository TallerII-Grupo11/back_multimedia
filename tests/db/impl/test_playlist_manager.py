import unittest
from unittest.mock import MagicMock

from app.db.impl.playlist_manager import PlaylistManager
from app.db.model.playlist import PlaylistModel
from app.db.model.artist import ArtistModel


def get_playlist_mock() -> PlaylistModel:
    return PlaylistModel(
        id="62be27922d98b5aaad951f95",
        title="title",
        songs=["song_id"],
        description="description",
        owner_id="user-id",
        is_collaborative=True,
    )


class TestPlaylistManager(unittest.TestCase):
    db = MagicMock()

    async def test_get_playlists(self):
        playlist1 = get_playlist_mock()
        playlist2 = get_playlist_mock()
        self.db["playlists"].find = MagicMock(return_value=[playlist1, playlist2])
        playlist_manager = PlaylistManager(self.db)
        result = await playlist_manager.get_playlists(None)

        assert len(result) == 2

    async def test_get_playlists_with_user_query(self):
        playlist = get_playlist_mock()
        self.db["playlists"].find = MagicMock(return_value=[playlist])
        playlist_manager = PlaylistManager(self.db)
        result = await playlist_manager.get_playlists("user_id")

        assert len(result) == 1

    async def test_get_playlist(self):
        playlist = get_playlist_mock()
        self.db["playlists"].find_one = MagicMock(return_value=playlist)
        playlist_manager = PlaylistManager(self.db)
        result = await playlist_manager.get_playlist("id")

        assert result is not None

    async def test_delete_song(self):
        self.db["playlists"].delete_one = MagicMock(return_value=True)
        playlist_manager = PlaylistManager(self.db)
        result = await playlist_manager.delete_playlist("id")

        assert result
