import os
from pymongo import MongoClient
from .db_strategy import DatabaseStrategy

class MongoStrategy(DatabaseStrategy):
    def __init__(self):
        host: str = os.getenv("MONGO_HOST", "localhost")
        port: int = os.getenv("MONGO_PORT", 27017)
        database = os.getenv("MONGO_DATABASE", "testdb")
        collection = os.getenv("MONGO_COLLECTION", "test_table")

        self.client = MongoClient(host, port)
        self.db = self.client[database]
        self.collection = self.db[collection]
        print(f"[MongoDB] Connected to {host}:{port}/{database}.{collection}")

    def create(self, data):
        result = self.collection.insert_one(data)
        print(f"[MongoDB] Inserted ID: {result.inserted_id}")

    def read(self, query):
        result = list(self.collection.find(query))
        print(result)
        return result

    def update(self, query, update):
        result = self.collection.update_one(query, {"$set": update})
        print(f"[MongoDB] Matched: {result.matched_count}, Modified: {result.modified_count}")

    def delete(self, query):
        result = self.collection.delete_one(query)
        print(f"[MongoDB] Deleted count: {result.deleted_count}")
