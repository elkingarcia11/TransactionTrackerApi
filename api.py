from decimal import *
from datetime import datetime
from bson import ObjectId


def insert_item(collection_name, item):
    collection_name.insert_one(item)

def get_item(collection_name, item):
    item = collection_name.find_one(item)
    if item is None:
        return True
    else:
        return False

def delete_item(collection_name, item_id):
    collection_name.delete_one({"_id":ObjectId(item_id)});

def addTransaction(collection_name, item):
    # searchItem = {"name" : name, "amount" : amount, "dateProcessed" : date(year, month, day).isoformat()}
    # item = {"name" : name, "invoice" : invoice, "receipt" : receipt, "amount" : amount, "dateProcessed" : date(year, month, day).isoformat(), "date" : datetime.today()}

    existsInDb = get_item(collection_name, item)

    if existsInDb:
        # Throw duplicate error
        print("DUPLICATE ENTRY")
    else:
        insert_item(collection_name, item)


def updateTransaction(collection_name, item):
    collection_name.find_one_and_update(
        {"_id":ObjectId(item.id)},
        {"$set":
            {"name" : item.name, "invoice" : item.invoice, "receipt" : item.receipt, "amount" : item.amount, "dateProcessed" : item.date.isoformat(), "date" : datetime.today()}
        }
    )
