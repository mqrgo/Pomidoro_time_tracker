import datetime

import bcrypt
from src.config import pwd_set, jwt_settings
import jwt


def encode_password(password: str, salt: bytes = pwd_set.salt) -> bytes:
    new_password = bcrypt.hashpw(password.encode(), salt)
    return new_password


def check_password(user_password: str, encoded_password: bytes) -> bool:
    return bcrypt.checkpw(user_password.encode(), encoded_password)


def create_jwt(payload: dict) -> str:
    now = datetime.datetime.utcnow()
    payload.update({'iat': now})
    token = jwt.encode(
        payload=payload,
        key=jwt_settings.salt,
        algorithm=jwt_settings.algorithm,
    )
    return token


def check_jwt(token: str):
    try:
        decoded_token = jwt.decode(
            token,
            key=jwt_settings.salt,
            algorithms=[jwt_settings.algorithm],
        )
        return decoded_token
    except jwt.InvalidTokenError:
        return False
