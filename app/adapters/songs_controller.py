from fastapi import APIRouter, status, Depends, Body, HTTPException
from typing import List
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.model.song import SongModel, UpdateSongModel

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
    created_song = await db.add_song(song)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_song)


@router.get(
    "/songs",
    response_description="List all songs",
    response_model=List[SongModel],
    status_code=status.HTTP_200_OK,
)
async def list_songs(db: DatabaseManager = Depends(get_database)):
    songs = await db.get_songs()
    return songs


@router.get(
    "/songs/{id}",
    response_description="Get a single song",
    response_model=SongModel,
    status_code=status.HTTP_200_OK,
)
async def show_song(id: str, db: DatabaseManager = Depends(get_database)):
    song = await db.get_song(song_id=id)
    if song is not None:
        return song

    raise HTTPException(status_code=404, detail=f"Song {id} not found")


@router.put(
    "/songs/{id}",
    response_description="Update a song",
    response_model=SongModel,
    status_code=status.HTTP_200_OK,
)
async def update_song(
    id: str,
    song: UpdateSongModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    song = await db.update_song(song_id=id, song=song)
    return song


@router.delete(
    "/songs/{id}",
    response_description="Delete a song",
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
)
async def delete_song(id: str, db: DatabaseManager = Depends(get_database)):
    delete_result = await db.delete_song(song_id=id)

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Song {id} not found")
