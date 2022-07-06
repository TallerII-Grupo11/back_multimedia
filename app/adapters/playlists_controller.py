from fastapi import APIRouter, status, Depends, Body, HTTPException

from fastapi.responses import JSONResponse

from app.db import DatabaseManager, get_database
from app.db.model.playlist import PlaylistModel, UpdatePlaylistModel
from app.db.impl.playlist_manager import PlaylistManager
from app.rest.metric_client import MetricClient
from app.rest import get_restclient_metrics
from bson import json_util
import json
from fastapi.encoders import jsonable_encoder


router = APIRouter(tags=["playlist"])


@router.post(
    "/playlists/",
    response_description="Add new playlist for user",
    response_model=PlaylistModel,
)
async def create_playlist(
    playlist: PlaylistModel = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_metric: MetricClient = Depends(get_restclient_metrics),
):
    manager = PlaylistManager(db.db)
    rest_metric.post_new_playlist(playlist)
    created_playlist = await manager.add_playlist(playlist)
    playlist_json = json.loads(json_util.dumps(created_playlist))
    playlist_json["id"] = playlist_json["_id"]
    del playlist_json["_id"]
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=playlist_json)


@router.get(
    "/playlists",
    response_description="List all Playlists",
    status_code=status.HTTP_200_OK,
)
async def list_playlists(
    user_id: str = None, db: DatabaseManager = Depends(get_database)
):
    manager = PlaylistManager(db.db)
    list_playlist = []
    if user_id:
        list_playlist = await manager.get_playlists(user_id)
    else:
        list_playlist = await manager.get_playlists()

    playlists = []
    for playlist in list_playlist:
        playlist_json = jsonable_encoder(playlist)
        playlist_json["id"] = playlist_json["_id"]
        del playlist_json["_id"]
        playlists.append(playlist_json)
    return playlists


@router.get(
    "/playlists/{id}",
    response_description="Get a single Playlist",
    status_code=status.HTTP_200_OK,
)
async def show_playlist(id: str, db: DatabaseManager = Depends(get_database)):
    manager = PlaylistManager(db.db)
    playlist = await manager.get_playlist(playlist_id=id)
    if playlist is not None:
        playlist_json = json.loads(json_util.dumps(playlist))
        playlist_json["id"] = playlist_json["_id"]
        del playlist_json["_id"]
        return playlist_json

    raise HTTPException(status_code=404, detail=f"Playlist {id} not found")


@router.put(
    "/playlists/{id}",
    response_description="Update a playlist",
    status_code=status.HTTP_200_OK,
)
async def update_playlist(
    id: str,
    playlist: UpdatePlaylistModel = Body(...),
    db: DatabaseManager = Depends(get_database),
):
    manager = PlaylistManager(db.db)
    try:
        playlist = await manager.update_playlist(playlist_id=id, playlist=playlist)
        playlist_json = json.loads(json_util.dumps(playlist))
        playlist_json["id"] = playlist_json["_id"]
        del playlist_json["_id"]
        return playlist_json
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


@router.delete(
    "/playlists/{id}",
    response_description="Delete a playlist",
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
)
async def delete_playlist(id: str, db: DatabaseManager = Depends(get_database)):
    manager = PlaylistManager(db.db)
    delete_result = await manager.delete_playlist(playlist_id=id)

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Playlist {id} not found")
