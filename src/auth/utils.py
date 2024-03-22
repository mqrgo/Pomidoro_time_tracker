import bcrypt
from src.config import pwd_set


def encode_password(password: str, salt: bytes = pwd_set.salt) -> bytes:
    new_password = bcrypt.hashpw(password.encode(), salt)
    return new_password


def check_password(user_password: str, encoded_password: bytes) -> bool:
    return bcrypt.checkpw(user_password.encode(), encoded_password)
