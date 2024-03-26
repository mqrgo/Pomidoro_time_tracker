import uuid

from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()


class DatabaseConfig(BaseSettings):
    user: str = getenv('DB_USER')
    pwd: str = getenv('DB_PASS')
    host: str = getenv('DB_HOST')
    port: str = getenv('DB_PORT')
    name: str = getenv('DB_NAME')

    @property
    def db_url(self):
        return f'postgresql+psycopg2://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.name}'


class PasswordSet(BaseSettings):
    salt: bytes = getenv('PASS_SALT').encode()


class JWTSettings(BaseSettings):
    salt: str = getenv('JWT_SALT').encode()
    algorithm: str = 'HS256'


db = DatabaseConfig()
pwd_set = PasswordSet()
jwt_settings = JWTSettings()

