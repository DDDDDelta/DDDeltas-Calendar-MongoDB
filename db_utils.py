from pymongo import MongoClient
from pymongo.errors import ConnectionError

class MongoDBConnection:
    def __init__(self, uri: str, database_name: str):
        self._uri = uri
        self._database_name = database_name
        self._client = None
        self._db = None
        self._connect()

    def _connect(self):
        try:
            self._client = MongoClient(self._uri)
            self._db = self._client[self._database_name]
        except ConnectionError as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def insert_one(self, collection_name: str, document: dict):
        collection = self._db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def find(self, collection_name: str, query: dict = None):
        collection = self._db[collection_name]
        return collection.find(query or {})

    def update_one(self, collection_name: str, query: dict, update: dict):
        collection = self._db[collection_name]
        return collection.update_one(query, update)

    def delete_one(self, collection_name: str, query: dict):
        collection = self._db[collection_name]
        return collection.delete_one(query)

    def close(self):
        if self._client:
            self._client.close()

