from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///:memory:?cache=shared&mode=memory")
    secret_key: str = os.getenv("SECRET_KEY", "secret-super-key-change-in-prod")

settings = Settings()

