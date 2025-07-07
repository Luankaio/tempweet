from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config


class Database:
    uri = config('DB_URI', default='mongodb://localhost:27017')
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    db = client.tempweet_db
    users = db["users"]
    tweets = db["tweets"]

# Instância global do database
database = Database()

def get_database():
    return database.db