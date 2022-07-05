from fastapi import APIRouter, status, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.impl.song_manager import SongManager
from app.db.model.song import SongModel, UpdateSongModel
from app.rest import get_restclient_metrics
from app.rest.metric_client import MetricClient
from bson import json_util
from fastapi.encoders import jsonable_encoder
import json


router = APIRouter(tags=["songs"])


@router.post(
    "/songs",
    response_description="Add new song",
)
async def create_song(
    song: SongModel = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_metric: MetricClient = Depends(get_restclient_metrics),
):
    manager = SongManager(db.db)
    rest_metric.post_new_song(song)
    created_song = await manager.add_song(song)
    song_json = json.loads(json_util.dumps(created_song))
    song_json["id"] = song_json["_id"]
    del song_json["_id"]
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=song_json)


@router.get(
    "/songs/{id}",
    response_description="Get a single song",
    status_code=status.HTTP_200_OK,
)
async def show_song(id: str, db: DatabaseManager = Depends(get_database)):
    manager = SongManager(db.db)
    try:
        song = await manager.get_song(song_id=id)
        song_json = json.loads(json_util.dumps(song))
        song_json["id"] = song_json["_id"]
        del song_json["_id"]
        return song_json
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


@router.get(
    "/songs",
    response_description="List all songs in by artist or genre",
    status_code=status.HTTP_200_OK,
)
async def list_songs_by(
    artist_name: str = None,
    genre: str = None,
    db: DatabaseManager = Depends(get_database)
):
    manager = SongManager(db.db)
    list_songs = []
    if artist_name:
        list_songs = await manager.list_songs_by_artist(artist_name)
    elif genre:
        list_songs = await manager.list_songs_by_genre(genre)
    else:
        list_songs = await manager.get_songs()

    songss = []
    for song in list_songs:
        song_json = jsonable_encoder(song)
        song_json["id"] = song_json["_id"]
        del song_json["_id"]
        songss.append(song_json)
    return songss


@router.put(
    "/songs/{id}",
    response_description="Update a song album",
    status_code=status.HTTP_200_OK,
)
async def update_song(
    id: str,
    song: UpdateSongModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = SongManager(db.db)
    song = await manager.update_song(song_id=id, song=song)
    song_json = json.loads(json_util.dumps(song))
    song_json["id"] = song_json["_id"]
    del song_json["_id"]
    return JSONResponse(song_json, status_code=status.HTTP_200_OK)
