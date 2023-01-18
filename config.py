from pydantic import BaseSettings

class Settings(BaseSettings):
    OAUTH2_SECRET_KEY : str
    OAUTH2_ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : str
    DATABASE_HOSTNAME : str
    DATABASE_USERNAME : str
    DATABASE_PASSWORD : str

settings = Settings()