from fastapi import Request, Response, Form
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import ValidationError
from src.auth.schemes import UserData
from src.config import db
from src.models import Users
from sqlalchemy.exc import ArgumentError
import datetime
import bcrypt
from src.config import pwd_set, jwt_settings
import jwt

engine = create_engine(url=db.db_url)
Session = sessionmaker(bind=engine)


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


def check_jwt(request: Request):
    token = request.cookies.get('session_token')
    if token is None:
        return False
    try:
        decoded_token = jwt.decode(
            token,
            key=jwt_settings.salt,
            algorithms=[jwt_settings.algorithm],
        )
        return decoded_token
    except jwt.InvalidTokenError:
        return False


def add_user_in_db(username: str, email: str, password: str):
    try:
        user = UserData(username=username, email=email, password=password)
        with Session() as session:
            try_username = session.query(Users.username).filter(Users.username == user.username).all()
            if len(try_username) != 0:
                raise ArgumentError('login already exist')
            try_email = session.query(Users.email).filter(Users.email == user.email).all()
            if len(try_email) != 0:
                raise ArgumentError('email already exist')
            new_password = encode_password(user.password)
            user = Users(username=user.username, email=user.email, password=new_password)
            session.add(user)
            session.commit()
            return True
    except ValidationError:
        return {'res': 'bad user data'}
    except ArgumentError as exc:
        print(exc.args[0])
        return {'res': exc.args[0]}
    except Exception as exc:
        print(exc.args)
        return {'res': exc.args[0]}


def check_user_exist(response: Response, username: str = Form(), password:str = Form()):
    with Session() as session:
        res = session.query(Users.id, Users.username, Users.password).filter(Users.username == username).all()
    if not res:
        return {'err': 'no user exist'}
    if not check_password(user_password=password, encoded_password=res[0][2]):
        return {'err': 'invalid password'}
    payload = {'id': res[0][0], 'username': res[0][1]}
    token = create_jwt(payload=payload)
    response.set_cookie(key='session_token', value=token, httponly=True, secure=True)
    return True
