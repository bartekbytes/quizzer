from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure


class AtlasClient():
    
    def __init__(self, atlas_uri: str, dbname: str):
        self.mongodb_client = MongoClient(atlas_uri)
        self.database = self.mongodb_client[dbname]

    def ping_server(self) -> bool:
        try:
            self.mongodb_client.admin.command('ping')
            return True
        except Exception as e:
            print(e)
            return False
        
    def drop_collection(self, collection_name: str) -> bool:

        # drop the collection in case it already exists
        try:
            self.database[collection_name].drop()
            return True

        except OperationFailure:
            print("An authentication error was received. Are your username and password correct in your connection string?")
            return False

    def insert(self, collection_name, operation: str, docs) -> bool:
        try: 
            if operation == "many":
                result = self.database[collection_name].insert_many(docs)
            elif operation == "one":
                result = self.database[collection_name].insert_one(docs)

        except OperationFailure:
            print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
            return False
        else:
            if operation == "many":
                inserted_count = len(result.inserted_ids)
                print("I inserted %x documents." %(inserted_count))
            elif operation == "one":
                print("I inserted a document.")
            return True
        
    def get_quizes(self, collection_name: str):
        docs = self.database[collection_name].find()
        return docs
    
    def get_quiz(self, collection_name: str, criteria: dict):
        doc = self.database[collection_name].find_one(criteria)

        if doc is not None:
            return doc
        else:
            return None