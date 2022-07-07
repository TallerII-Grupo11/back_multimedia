import json
import unittest
import httpx
import respx

from app.db.model.album import AlbumModel
from app.db.model.artist import ArtistModel
from app.db.model.playlist import PlaylistModel
from app.db.model.song import SongModel
from app.rest.metric_client import MetricClient
from bson import json_util


def get_mocked_response(status_code: int) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=dict(),
    )


def get_song_mock() -> SongModel:
    return SongModel(
        id="62be27922d98b5aaad951f95",
        title="title",
        artists=[ArtistModel(artist_id="id", artist_name="name")],
        description="description",
        genre="genre",
        song_file="file",
    )


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


def get_playlist_mock() -> PlaylistModel:
    return PlaylistModel(
        id="62be27922d98b5aaad951f95",
        title="title",
        songs=["song_id"],
        description="description",
        owner_id="user-id",
        is_collaborative=True,
    )


class TestMetricClient(unittest.TestCase):
    test_url = "https://test-api.com"

    @respx.mock
    def test_new_song(self, respx_mock):
        song_mock = get_song_mock()
        song = json.loads(json_util.dumps(song_mock))
        route = respx_mock.post(f"{self.test_url}/song", json=song).mock(
            return_value=get_mocked_response(200))
        client = MetricClient(self.test_url)
        client.post_new_song(song_mock)

        assert route.called

    @respx.mock
    def test_new_album(self, respx_mock):
        album_mock = get_album_mock()
        album = json.loads(json_util.dumps(album_mock))
        route = respx_mock.post(f"{self.test_url}/album", json=album).mock(
            return_value=get_mocked_response(200))
        client = MetricClient(self.test_url)
        client.post_new_album(album_mock)

        assert route.called

    @respx.mock
    def test_new_playlist(self, respx_mock):
        playlist_mock = get_playlist_mock()
        playlist = json.loads(json_util.dumps(playlist_mock))
        route = respx_mock.post(f"{self.test_url}/playlist", json=playlist).mock(
            return_value=get_mocked_response(200))
        client = MetricClient(self.test_url)
        client.post_new_playlist(playlist_mock)

        assert route.called
