from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Token (BaseModel):
    access_token: str
    token_type: str

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
    date : str

class TransactionRequestResponse(BaseModel):
    status : int
    message : str

class IdList(BaseModel):
    ids : List[str]
