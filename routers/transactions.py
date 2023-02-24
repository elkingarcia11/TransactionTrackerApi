import pymongo
from fastapi import APIRouter, Depends, HTTPException
from api import get_item
from functions import isValidTransaction
from schemas import IdList, TokenData, Transaction, TransactionRequestResponse, TransactionResponse
from oauth2 import get_current_user
from bson import ObjectId, objectid
from database import clients
import pydantic
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/api/tracker/transactions", tags=['Transactions'])

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

# Get transactions
@router.get("/", status_code=200)
async def getTransactions(user_credentials: TokenData = Depends(get_current_user)):
    print(user_credentials)
    if user_credentials.userId is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    trans = clients.find().sort("date", pymongo.DESCENDING)
    l = list(trans)
    return {"data": l}

# Add transaction
@router.post("/", status_code=200)
async def addTransaction(transaction: Transaction, user_credentials: TokenData = Depends(get_current_user)):
    print("YOO")
    if user_credentials.userId is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role == "admin":
        # validate fields
        if isValidTransaction(transaction):
            # if item exists in DB
            json_compatible_item_data = jsonable_encoder(transaction)
            if get_item(clients, json_compatible_item_data):
                raise HTTPException(status_code=409, detail="This is a duplicate entry")
            else:
                json_compatible_item_data = jsonable_encoder(transaction)
                i = clients.insert_one(json_compatible_item_data)
                return TransactionRequestResponse(status=200, message=str(i.inserted_id))
        else:
            return TransactionRequestResponse(status=400, message="Could not add transaction to database")
    else:
        return TransactionRequestResponse(status=403, message="Invalid credentials")

# Add duplicate transaction
@router.post("/override", status_code=201)
async def addTransaction(transaction: Transaction, user_credentials: TokenData = Depends(get_current_user)):
    print("YOO3")
    if user_credentials.userId is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role == "admin":
        # validate fields
        if isValidTransaction(transaction):
            clients.insert_one(transaction)
        else:
            return TransactionRequestResponse(status=400, message="Could not add transaction to database")
    else:
        return TransactionRequestResponse(status=403, message="Invalid credentials")


# Update transaction
@router.put("/", status_code=200)
async def updateTransaction(transaction: TransactionResponse, user_credentials: TokenData = Depends(get_current_user)):
    print("YOO1")
    if user_credentials.userId is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role == "admin":
        if transaction.oid is not None and objectid.ObjectId.is_valid(transaction.oid):
            clients.find_one_and_update({"_id": ObjectId(transaction.oid)},
                                    {"$set":
                                     {"name": transaction.name.lower(), "invoice": transaction.invoice, "receipt": transaction.receipt,
                                      "amount": transaction.amount, "dateProcessed": transaction.dateProcessed, "date": transaction.date}
                                     }
                                    )
            return {"data": transaction}
        else:
            return TransactionRequestResponse(status=403, message="Could not update information")
    else:
        return TransactionRequestResponse(status=403, message="Invalid credentials")

# Delete transaction(s)
@router.delete("/", status_code=200)
async def deleteTransactions(id_list : IdList, user_credentials: TokenData = Depends(get_current_user)):
    print("YOO2")
    json_compatible_item_data = jsonable_encoder(id_list)
    if user_credentials.userId is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role == "admin":
        deleted_transactions : IdList = []
        for i in json_compatible_item_data["ids"]:
            if i is not None and objectid.ObjectId.is_valid(i):
                clients.delete_one({"_id": ObjectId(i)})
                deleted_transactions.append(i)
        return {"Deleted transactions": deleted_transactions}
    else:
        raise HTTPException(status_code=403, detail="Invalid credentials")
