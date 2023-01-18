from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId


class Token (BaseModel):
    access_token: str
    token_type: str

class LogInRequest(BaseModel):  
    email: str
    password : str

class TokenData(BaseModel):
    userId : Optional[str] = None
    role : Optional[str] = None

class Transaction(BaseModel):
    name : str
    invoice : str
    receipt : str
    amount : str
    dateProcessed : str
    date = datetime.today()

class TransactionResponse(BaseModel):
    id : str
    name : str
    invoice : str
    receipt : str
    amount : str
    dateProcessed : str
    date = datetime.today()


class TransactionRequestResponse(BaseModel):
    status : int
    message : str

class UserRequestResponse(BaseModel):
    _id : ObjectId
    role : str