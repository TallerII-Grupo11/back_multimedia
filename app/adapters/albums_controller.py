from fastapi import APIRouter, status, Depends, Body, HTTPException

from fastapi.responses import JSONResponse

from app.db import DatabaseManager, get_database
from app.db.model.album import AlbumModel, UpdateAlbumModel, SongAlbumModel
from app.db.impl.album_manager import AlbumManager


router = APIRouter(tags=["albums"])


@router.post(
    "/albums",
    response_description="Add new album",
    response_model=AlbumModel,
)
async def create_album(
    album: AlbumModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = AlbumManager(db.db)
    created_album = await manager.add_album(album)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_album)


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
    db: DatabaseManager = Depends(get_database)
):
    manager = AlbumManager(db.db)
    if subscription:
        return await manager.get_albums_by_subscription(subscription)
    if artist_name:
        return await manager.get_albums_by_artist(artist_name)
    if genre:
        return await manager.get_albums_by_genre(genre)
    if song_id:
        album = await manager.get_albums_by_song(song_id)
        if album:
            return JSONResponse(album, status_code=status.HTTP_200_OK)
        raise HTTPException(
            status_code=400, detail=f"Album for song {song_id} NOT_FOUND"
        )

    albums = await manager.get_albums()
    return albums


@router.get(
    "/albums/{id}",
    response_description="Get a single album",
    response_model=UpdateAlbumModel,
    status_code=status.HTTP_200_OK,
)
async def show_album(id: str, db: DatabaseManager = Depends(get_database)):
    manager = AlbumManager(db.db)
    album = await manager.get_album(album_id=id)
    if album is not None:
        return album

    raise HTTPException(status_code=404, detail=f"Album {id} not found")


@router.put(
    "/albums/{id}",
    response_description="Update a album",
    status_code=status.HTTP_200_OK,
)
async def update_album(
    id: str,
    album: UpdateAlbumModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = AlbumManager(db.db)
    try:
        album = await manager.update_album(album_id=id, album=album)
        return JSONResponse(album, status_code=status.HTTP_200_OK)
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
    db: DatabaseManager = Depends(get_database)
):
    manager = AlbumManager(db.db)
    album = await manager.add_song(album_id=id, album=album)
    return JSONResponse(album, status_code=status.HTTP_200_OK)
