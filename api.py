from decimal import *
from datetime import datetime
from bson import ObjectId

def get_item(collection_name, item):
    item = collection_name.find_one(item)
    if item is None:
        return False
    else:
        return True

def updateTransaction(collection_name, item):
    collection_name.find_one_and_update(
        {"_id":ObjectId(item.id)},
        {"$set":
            {"name" : item.name.lower(), "invoice" : item.invoice, "receipt" : item.receipt, "amount" : item.amount, "dateProcessed" : item.date.isoformat(), "date" : datetime.today()}
        }
    )
