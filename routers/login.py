from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from functions import emailIsValid
from oauth2 import create_access_token
from schemas import Token
from database import users

router = APIRouter(prefix="/api/tracker/login", tags=["Authentication"])

# Login
@router.get("/")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    if emailIsValid(user_credentials.username):
        query = {"$and":[{"username":user_credentials.username},
                                  {"password":user_credentials.password}]}   
        user = users.find(query)
        if user == None:
            return HTTPException(status_code=403, detail= "Invalid Credentials")
        else:
            for u in user:
                access_token = create_access_token(data = {"userId": str(u["_id"]), "role":u["role"]})
                return Token(access_token=access_token, token_type="Bearer")
            return HTTPException(status_code=404, detail= "User does not exist")
    else:
        return HTTPException(status_code=403, detail= "Invalid Credentials")