import httpx
import json

from fastapi import Body
from typing import List
from app.db.model.song import SongModel
from app.db.model.album import AlbumModel
from app.db.model.playlist import PlaylistModel
from fastapi.encoders import jsonable_encoder


class MetricClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def post_new_song(self, song: SongModel = Body(...)):
        song = jsonable_encoder(song)
        r = httpx.post(f'{self.api_url}/song', data=json.dumps(song))

    def post_new_album(self, album: AlbumModel = Body(...)):
        album = jsonable_encoder(album)
        r = httpx.post(f'{self.api_url}/album', data=json.dumps(album))

    def post_new_playlist(self, playlist: PlaylistModel = Body(...)):
        playlist = jsonable_encoder(playlist)
        r = httpx.post(f'{self.api_url}/playlist', data=json.dumps(playlist))
