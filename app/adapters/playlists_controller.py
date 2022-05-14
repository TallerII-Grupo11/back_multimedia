from fastapi import APIRouter, status, Depends, Body, HTTPException

from typing import List
from fastapi.responses import JSONResponse

from app.db import DatabaseManager, get_database
from app.db.model.playlist import PlaylistModel, UpdatePlaylistModel, SongPlaylistModel
from app.db.impl.playlist_manager import PlaylistManager


router = APIRouter(tags=["playlist"])


@router.post(
    "/playlists/",
    response_description="Add new playlist for user",
    response_model=PlaylistModel,
)
async def create_playlist(
    playlist: PlaylistModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = PlaylistManager(db.db)
    created_playlist = await manager.add_playlist(playlist)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_playlist)


@router.get(
    "/playlists",
    response_description="List all Playlists",
    response_model=List[PlaylistModel],
    status_code=status.HTTP_200_OK,
)
async def list_playlists(
    user_id: str = None,
    db: DatabaseManager = Depends(get_database)
):
    manager = PlaylistManager(db.db)
    if user_id:
        return await manager.get_playlists(user_id)
    return await manager.get_playlists()


@router.get(
    "/playlists/{id}",
    response_description="Get a single Playlist",
    response_model=PlaylistModel,
    status_code=status.HTTP_200_OK,
)
async def show_playlist(id: str, db: DatabaseManager = Depends(get_database)):
    manager = PlaylistManager(db.db)
    playlist = await manager.get_playlist(playlist_id=id)
    if playlist is not None:
        return playlist

    raise HTTPException(status_code=404, detail=f"Playlist {id} not found")


@router.put(
    "/playlists/{id}",
    response_description="Update a playlist",
    status_code=status.HTTP_200_OK,
)
async def update_playlist(
    id: str,
    playlist: UpdatePlaylistModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = PlaylistManager(db.db)
    try:
        playlist = await manager.update_playlist(playlist_id=id, playlist=playlist)
        return playlist
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


@router.patch(
    "/playlists/{id}",
    response_description="Add song to playlist",
    status_code=status.HTTP_200_OK,
)
async def add_song_to_playlist(
    id: str,
    playlist: SongPlaylistModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = PlaylistManager(db.db)
    try:
        playlist = await manager.add_song(playlist_id=id, playlist=playlist)
        return playlist
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
