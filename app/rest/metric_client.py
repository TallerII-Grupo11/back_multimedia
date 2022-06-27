import httpx
import json
import logging

from typing import List
from app.db.model.song import SongModel
from fastapi.encoders import jsonable_encoder


class MetricClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def post_new_song(self, song: SongModel = Body(...)):
        song = jsonable_encoder(song)
        r = httpx.post(f'{self.api_url}/song', data=json.dumps(song.dict()))
        d = r.json()
        return r.json()