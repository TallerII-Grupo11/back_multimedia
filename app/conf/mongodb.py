import os
import motor.motor_asyncio
import pymongo
from pydantic import BaseSettings


class MongoDB(BaseSettings):
	
	mongo_url = os.environ["MONGODB_URL"]
	client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
	
	db = client.multimedia

	class Config:
		BASE_DIR = os.path.dirname(os.path.abspath("../.env"))
		env_file = os.path.join(BASE_DIR, ".env")

