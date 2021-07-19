import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from dotenv import load_dotenv

from src.bot.consts import big_num

load_dotenv()
cluster = AsyncIOMotorClient(os.getenv("MONGO"))
db = cluster["toxic"]

cluster_non_async = MongoClient(os.getenv("MONGO"))
db_non_async = cluster_non_async["toxic"]


class Data:
    def __init__(self, collection_name: str):
        self.collection = db[collection_name]
        self.collection_non_async = db_non_async[collection_name]

    async def get(self, _id: str or int):
        return d["data"] if (d := await self.collection.find_one({"_id": str(_id)})) else None

    def get_non_async(self, _id: str or int):
        return d["data"] if (d := self.collection_non_async.find_one({"_id": str(_id)})) else None

    async def set(self, _id: str or int, data: dict):
        await self.collection.update_one({"_id": str(_id)}, {"$set": {k: v for k, v in data.items()}})

    def set_non_async(self, _id: str or int, data: dict):
        self.collection_non_async.update_one({"_id": str(_id)}, {"$set": {k: v for k, v in data.items()}})

    async def add(self, _id: str or int, data: dict):
        post = {"_id": str(_id)}
        post.update(data)
        await self.collection.insert_one(post)

    def add_non_async(self, _id: str or int, data: dict):
        post = {"_id": str(_id)}
        post.update(data)
        self.collection_non_async.insert_one(post)

    async def delete(self, _id: str or int, data: dict):
        await self.collection.update_one({"_id": str(_id)}, {"$unset": {k: v for k, v in data.items()}})

    async def all(self):
        return await (self.collection.find()).to_list(length=big_num)

    def all_non_async(self):
        return self.collection_non_async.find()


guilds_data = Data("guilds")
game_data = Data("game")
stocks_data = Data("stocks")
