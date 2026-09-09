from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    #1. each field here maps to an environment variable in .env
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 30

    """
    class Config:  
        env_file = ".env"           #2. tell Pydantic where to read environment variables from
    """
    model_config = SettingsConfigDict(env_file=".env")  #modern Pydantic v2 syntax

settings = Settings()   #3. create a single shared instane to import across my project
