import pymongo
from config import settings

connection = pymongo.MongoClient(settings.DATABASE_HOSTNAME)   
transactions = connection["transactions"]
clients = transactions["clients"]
users = transactions["users"]