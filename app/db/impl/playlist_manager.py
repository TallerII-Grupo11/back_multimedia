from typing import List
import logging

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.model.playlist import PlaylistModel, UpdatePlaylistModel, SongPlaylistModel
from fastapi import Body
from fastapi.encoders import jsonable_encoder


class PlaylistManager():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def add_playlist(self, playlist: PlaylistModel = Body(...)) -> PlaylistModel:
        playlist = jsonable_encoder(playlist)
        await self.db["playlists"].insert_one(playlist)
        return playlist

    async def get_playlists(self, user_id: str = None) -> List[PlaylistModel]:
        playlist_list = []
        if not user_id:
            playlist_q = self.db["playlists"].find()
        else:
            playlist_q = self.db["playlists"].find({"user_owner": user_id})

        async for playlist in playlist_q:
            playlist_list.append(PlaylistModel(**playlist))
        return playlist_list

    async def get_playlist(self, playlist_id: str) -> PlaylistModel:
        playlist = await self.db["playlists"].find_one({"_id": playlist_id})
        return playlist

    async def delete_playlist(self, playlist_id: str):
        delete_result = await self.db["playlists"].delete_one({"_id": playlist_id})
        return delete_result

    async def update_playlist(
        self,
        playlist_id: str,
        playlist: UpdatePlaylistModel = Body(...)
    ) -> PlaylistModel:
        try:
            playlist = {k: v for k, v in playlist.dict().items() if v is not None}
            available = await self.check_update_available(playlist_id, playlist)
            if available:
                await self.db["playlists"].update_one({"_id": playlist_id},
                                                      {"$set": playlist}
                                                      )
            playlist_model = await self.get_playlist(playlist_id)
            return playlist_model
        except Exception as e:
            logging.info(f"{e}")
            return e

    async def add_song(
        self,
        playlist_id: str,
        playlist: SongPlaylistModel = Body(...)
    ) -> PlaylistModel:
        try:
            playlist = {k: v for k, v in playlist.dict().items() if v is not None}
            available = await self.check_update_available(playlist_id, playlist)
            if available and "songs" in playlist:
                await self.db["playlists"]\
                        .update_one({"_id": playlist_id},
                                    {"$push": {"songs": {"$each": playlist["songs"]}}}
                                    )
            playlist_model = await self.get_playlist(playlist_id)
            return playlist_model
        except Exception as e:
            logging.info(f"{e}")
            return e

    async def check_update_available(
        self,
        playlist_id: str,
        playlist: dict
    ) -> bool:
        playlist_to_update = await self.get_playlist(playlist_id)
        playlist_to_update = jsonable_encoder(playlist_to_update)

        if not (playlist["owner_id"] == playlist_to_update["owner_id"] or
                playlist_to_update["is_collaborative"]):
            msg = f"User {playlist['owner_id']} can't edit playlist {playlist_id}"
            logging.error(msg)
            raise RuntimeError(msg)
        return True
