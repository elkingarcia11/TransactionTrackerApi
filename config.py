from pydantic import BaseSettings

class Settings(BaseSettings):
    OAUTH2_SECRET_KEY : str
    OAUTH2_ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    DATABASE_HOSTNAME : str
    DATABASE_USERNAME : str
    DATABASE_PASSWORD : str

    class Config:
        env_file = ".env"

settings = Settings()
