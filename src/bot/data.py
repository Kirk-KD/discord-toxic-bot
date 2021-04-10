import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
cluster = MongoClient(os.getenv("MONGO"))
db = cluster["toxic"]


class Data:
    def __init__(self, collection_name: str):
        self.collection = db[collection_name]

    def get(self, _id: str or int):
        return d["data"] if (d := self.collection.find_one({"_id": str(_id)})) else None

    def set(self, _id: str or int, data: dict):
        self.collection.update_one({"_id": str(_id)}, {"$set": {k: v for k, v in data.items()}})

    def add(self, _id: str or int, data: dict):
        post = {"_id": str(_id)}
        post.update(data)
        self.collection.insert_one(post)

    def all(self):
        return self.collection.find({})


guilds_data = Data("guilds")
game_data = Data("game")
stocks_data = Data("stocks")
