from fastapi import APIRouter, status, Depends, Body, HTTPException

from fastapi.responses import JSONResponse

from app.db import DatabaseManager, get_database
from app.db.model.album import AlbumModel, UpdateAlbumModel, SongAlbumModel
from app.db.impl.album_manager import AlbumManager
from app.db.impl.song_manager import SongManager
from app.rest.metric_client import MetricClient
from app.rest import get_restclient_metrics
from app.adapters.utils.utils import get_data, get_list
from bson import json_util
import json
from fastapi.encoders import jsonable_encoder


router = APIRouter(tags=["albums"])


@router.post(
    "/albums",
    response_description="Add new album",
    response_model=AlbumModel,
)
async def create_album(
    album: AlbumModel = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_metric: MetricClient = Depends(get_restclient_metrics),
):
    manager = AlbumManager(db.db)
    rest_metric.post_new_album(album)
    created_album = await manager.add_album(album)
    album_json = json.loads(json_util.dumps(created_album))
    album_json["id"] = album_json["_id"]
    del album_json["_id"]
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=album_json)


@router.get(
    "/albums",
    response_description="List albums by query",
    # response_model=List[AlbumModel],
    status_code=status.HTTP_200_OK,
)
async def list_albums(
    subscription: str = None,
    artist_name: str = None,
    song_id: str = None,
    genre: str = None,
    db: DatabaseManager = Depends(get_database),
):
    manager = AlbumManager(db.db)
    manager_song = SongManager(db.db)
    list_albums = []
    if subscription:
        list_albums = await manager.get_albums_by_subscription(subscription)
    if artist_name:
        list_albums = await manager.get_albums_by_artist(artist_name)
    if genre:
        list_albums = await manager.get_albums_by_genre(genre)
    if song_id:
        album = await manager.get_albums_by_song(song_id)
        if album:
            album_json = get_data(album)
            songs = await manager_song.get_songs(album_json["songs"])
            list_songs = get_list(songs)
            del album_json["songs"]
            album_json["songs"] = list_songs
            return JSONResponse(album_json, status_code=status.HTTP_200_OK)
        raise HTTPException(
            status_code=400, detail=f"Album for song {song_id} NOT_FOUND"
        )
    if not subscription and not artist_name and not genre:
        list_albums = await manager.get_albums()

    albumss = []
    for album in list_albums:
        album_json = jsonable_encoder(album)
        album_json["id"] = album_json["_id"]
        del album_json["_id"]

        songs = await manager_song.get_songs(album_json["songs"])
        list_songs = get_list(songs)
        del album_json["songs"]
        album_json["songs"] = list_songs
        albumss.append(album_json)
    return albumss


@router.get(
    "/albums/{id}",
    response_description="Get a single album",
    status_code=status.HTTP_200_OK,
)
async def show_album(id: str, db: DatabaseManager = Depends(get_database)):
    manager = AlbumManager(db.db)
    manager_song = SongManager(db.db)
    album = await manager.get_album(album_id=id)
    if album is not None:
        album_json = get_data(album)
        songs = await manager_song.get_songs(album_json["songs"])
        list_songs = get_list(songs)
        del album_json["songs"]
        album_json["songs"] = list_songs
        return album_json

    raise HTTPException(status_code=404, detail=f"Album {id} not found")


@router.put(
    "/albums/{id}",
    response_description="Update a album",
    status_code=status.HTTP_200_OK,
)
async def update_album(
    id: str,
    album: UpdateAlbumModel = Body(...),
    db: DatabaseManager = Depends(get_database),
):
    manager = AlbumManager(db.db)
    try:
        album = await manager.update_album(album_id=id, album=album)
        album_json = json.loads(json_util.dumps(album))
        album_json["id"] = album_json["_id"]
        del album_json["_id"]
        return JSONResponse(album_json, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


@router.patch(
    "/albums/{id}/songs",
    response_description="Add songs to album",
    status_code=status.HTTP_200_OK,
)
async def add_song_to_album(
    id: str,
    album: SongAlbumModel = Body(...),
    db: DatabaseManager = Depends(get_database),
):
    manager = AlbumManager(db.db)
    album = await manager.add_song(album_id=id, album=album)
    return JSONResponse(album, status_code=status.HTTP_200_OK)
