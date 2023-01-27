import pymongo
from config import settings


print("HOSTNAME: ", settings.DATABASE_HOSTNAME)
connection = pymongo.MongoClient(settings.DATABASE_HOSTNAME)   
transactions = connection["transactions"]
clients = transactions["clients"]
users = transactions["users"]