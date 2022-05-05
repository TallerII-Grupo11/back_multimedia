from fastapi import APIRouter, status, Depends, Body, HTTPException

from typing import List
from fastapi.responses import JSONResponse

from app.db import DatabaseManager, get_database
from app.db.model.album import AlbumModel, UpdateAlbumModel

router = APIRouter(tags=["albums"])


@router.post("/albums",
    response_description="Add new album",
    response_model=AlbumModel,
    )
async def create_album(
    album: AlbumModel = Body(...), 
    db: DatabaseManager = Depends(get_database)
    ):
    created_album = await db.add_album(album)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_album)


@router.get(
    "/albums",
    response_description="List all albums",
    response_model=List[AlbumModel],
    status_code=status.HTTP_200_OK,
    )
async def list_albums(db: DatabaseManager = Depends(get_database)):
    albums = await db.get_albums()
    return albums


@router.get(
    "/albums/{id}",
    response_description="Get a single album",
    response_model=AlbumModel,
    status_code=status.HTTP_200_OK,
    )
async def show_album(id: str, db: DatabaseManager = Depends(get_database)):
    album = await db.get_album(album_id=id)
    if album is not None: 
        return album 

    raise HTTPException(status_code=404, detail=f"Album {id} not found")


@router.put("/albums/{id}",
    response_description="Update a album",
    response_model=AlbumModel,
    status_code=status.HTTP_200_OK,
)
async def update_album(id: str, album: UpdateAlbumModel = Body(...), db: DatabaseManager = Depends(get_database)):
    album = await db.update_album(album_id=id, album=album)
    return album

@router.delete("/albums/{id}",
    response_description="Delete a album",
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
    )
async def delete_album(id: str, db: DatabaseManager = Depends(get_database)):
    delete_result = await db.delete_album(album_id=id)

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Album {id} not found")
