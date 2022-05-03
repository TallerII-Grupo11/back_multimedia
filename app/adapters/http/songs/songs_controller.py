from fastapi import APIRouter, status, Depends

from app.conf.config import Settings
from app.conf.mongodb import MongoDB
from app.dependencies.dependencies import get_settings, get_mongodb
from app.adapters.http.songs import song
from typing import Optional, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder



router = APIRouter(tags=["songs"])

mongo_url="mongodb+srv://admin_user:v7JrrBsR826G9hlO@multimedia.a0iq4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
#mongo = Depends(get_mongodb)
#mongo_url = os.environ["MONGODB_URL"]
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
	
db = client.multimedia
#db = mongo.db


@app.post("/songs", 
	response_description="Add new song", 
	response_model=SongModel,
	status_code=status.HTTP_200_OK,
)
async def create_song(song: SongModel = Body(...)):
	song = jsonable_encoder(song)
	new_song = await db["songs"].insert_one(song)
	created_song = await db["songs"].find_one({"_id": new_song.inserted_id})
	return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_song)


@app.get(
	"/songs", 
	response_description="List all songs", 
	response_model=List[SongModel],
	status_code=status.HTTP_200_OK,
)
async def list_songs():
	songs = await db["songs"].find().to_list(1000)
	return songs


@app.get(
	"/songs/{id}", 
	response_description="Get a single song", 
	response_model=SongModel,
	status_code=status.HTTP_200_OK,
)
async def show_song(id: str):
	if (song := await db["songs"].find_one({"_id": id})) is not None:
		return song

	raise HTTPException(status_code=404, detail=f"Song {id} not found")


@app.put("/songs/{id}", 
	response_description="Update a song",
	response_model=SongModel,
	status_code=status.HTTP_200_OK,
)
async def update_song(id: str, song: UpdateSongModel = Body(...)):
	song = {k: v for k, v in song.dict().items() if v is not None}

	if len(song) >= 1:
		update_result = await db["songs"].update_one({"_id": id}, {"$set": song})

		if update_result.modified_count == 1:
			if (
				updated_song := await db["songs"].find_one({"_id": id})
			) is not None:
				return updated_song

	if (existing_song := await db["songs"].find_one({"_id": id})) is not None:
		return existing_song

	raise HTTPException(status_code=404, detail=f"Song {id} not found")


@app.delete("/songs/{id}", 
	response_description="Delete a song", 
	include_in_schema=False,
	status_code=status.HTTP_200_OK,
)
async def delete_song(id: str):
	delete_result = await db["songs"].delete_one({"_id": id})

	if delete_result.deleted_count == 1:
		return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

	raise HTTPException(status_code=404, detail=f"Song {id} not found")
