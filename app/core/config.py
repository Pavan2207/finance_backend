from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: str = "postgresql://finance_user:finance_pass@localhost:5432/finance_db"
    secret_key: str = "secret"

settings = Settings()

