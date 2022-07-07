import httpx
import json

from fastapi import Body
from app.db.model.song import SongModel
from app.db.model.album import AlbumModel
from app.db.model.playlist import PlaylistModel
from bson import json_util


class MetricClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def post_new_song(self, song: SongModel = Body(...)):
        song = json.loads(json_util.dumps(song))
        httpx.post(f'{self.api_url}/song', json=song)

    def post_new_album(self, album: AlbumModel = Body(...)):
        album = json.loads(json_util.dumps(album))
        httpx.post(f'{self.api_url}/album', json=album)

    def post_new_playlist(self, playlist: PlaylistModel = Body(...)):
        playlist = json.loads(json_util.dumps(playlist))
        httpx.post(f'{self.api_url}/playlist', json=playlist)
