from fastapi import APIRouter, status, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.impl.song_manager import SongManager
from app.db.model.song import SongModel, UpdateSongModel
from typing import List

router = APIRouter(tags=["songs"])


@router.post(
    "/songs",
    response_description="Add new song",
    response_model=SongModel
)
async def create_song(
    song: SongModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = SongManager(db.db)
    created_song = await manager.add_song(song)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_song)


@router.get(
    "/songs/{id}",
    response_description="Get a single song",
    response_model=UpdateSongModel,
    status_code=status.HTTP_200_OK,
)
async def show_song(id: str, db: DatabaseManager = Depends(get_database)):
    manager = SongManager(db.db)
    try:
        song = await manager.get_song(song_id=id)
        return song
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


@router.get(
    "/songs/",
    response_description="List all songs in by artist or album",
    response_model=List[SongModel],
    status_code=status.HTTP_200_OK,
)
async def list_songs_by(
    artist_id: str = None,
    db: DatabaseManager = Depends(get_database)
):
    manager = SongManager(db.db)
    return await manager.list_songs_by_artist(artist_id)


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
    return JSONResponse(song, status_code=status.HTTP_200_OK)
