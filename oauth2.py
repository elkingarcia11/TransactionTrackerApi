from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from config import settings
from schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/")

def create_access_token(data: dict): 
    # get copy to manipulate
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=1440)

    # add property to data
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.OAUTH2_SECRET_KEY, algorithm=settings.OAUTH2_ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.OAUTH2_SECRET_KEY, algorithms= [settings.OAUTH2_ALGORITHM])
        id : str = payload.get("userId")
        r : str = payload.get("role")
        if id is None:
            raise credentials_exception
        if r is None:
            raise credentials_exception

        token_data = TokenData(userId=id, role=r)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=403, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)