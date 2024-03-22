import uuid

from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel

load_dotenv()


class DatabaseConfig(BaseModel):
    user: str = getenv('DB_USER')
    pwd: str = getenv('DB_PASS')
    host: str = getenv('DB_HOST')
    port: str = getenv('DB_PORT')
    name: str = getenv('DB_NAME')
    db_url: str = f'postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{name}'


class PasswordSet(BaseModel):
    salt: bytes = getenv('SALT').encode()


db = DatabaseConfig()
pwd_set = PasswordSet()

