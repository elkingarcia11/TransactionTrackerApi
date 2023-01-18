from typing import Union
import pymongo
from fastapi import APIRouter, Depends, HTTPException
from api import get_item
from functions import isValidTransaction
from schemas import TokenData, Transaction, TransactionRequestResponse, TransactionResponse
from oauth2 import get_current_user
from bson import ObjectId
from database import clients

router = APIRouter(prefix="/api/tracker/transactions", tags=['Transactions'])

# Get transactions
@router.get("/", status_code=200)
async def getTransactions(user_credentials: TokenData = Depends(get_current_user)):
    if user_credentials.userId is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    t = clients.find().sort("date", pymongo.DESCENDING)
    return {"data": t}

# Add transaction
@router.post("/", status_code=201)
async def addTransaction(transaction: Transaction, user_credentials: TokenData = Depends(get_current_user)):
    if user_credentials.userId is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role == "admin":
        # validate fields
        if isValidTransaction(transaction):
            # if item exists in DB
            if get_item(clients, transaction):
                return TransactionRequestResponse(status=409, message="This is a duplicate entry")
            else:
                clients.insert_one(transaction)
        else:
            return TransactionRequestResponse(status=400, message="Could not add transaction to database")
    else:
        return TransactionRequestResponse(status=403, message="Invalid credentials")

# Add duplicate transaction
@router.post("/overrideAdd", status_code=201)
async def addTransaction(transaction: Transaction, user_credentials: TokenData = Depends(get_current_user)):
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
    if user_credentials.userId is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role is None:
        return TransactionRequestResponse(status=403, message="Invalid credentials")
    if user_credentials.role == "admin":
        clients.find_one_and_update({"_id": ObjectId(transaction.id)},
                                    {"$set":
                                     {"name": transaction.name, "invoice": transaction.invoice, "receipt": transaction.receipt,
                                      "amount": transaction.amount, "dateProcessed": transaction.dateProcessed, "date": transaction.date}
                                     }
                                    )
        return {"data": transaction}
    else:
        return TransactionRequestResponse(status=403, message="Invalid credentials")

# Delete transaction(s)
@router.delete("/", status_code=204)
async def deleteTransactions(id: Union[str, None] = None, user_credentials: TokenData = Depends(get_current_user)):
    if user_credentials.userId is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if user_credentials.role == "admin":
        deleted_transactions = [str]
        for i in id:
            clients.delete_one({"_id": ObjectId(i)})
            deleted_transactions.append(i)
        return {"Deleted transactions": deleted_transactions}
    else:
        raise HTTPException(status_code=403, detail="Invalid credentials")
