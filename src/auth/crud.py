from typing import Tuple, Any, Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemes import UserData
from pydantic import ValidationError
from src.auth.utils import encode_password, check_password
from src.config import db
from src.models import Users
from sqlalchemy.exc import ArgumentError
engine = create_engine(url=db.db_url)
Session = sessionmaker(bind=engine)


# with Session() as session:
# user = UserData(username='username', email='emaila', password='passwordQWE1234')
# new_password = encode_password(user.password)
# user = Users(username=user.username, email=user.email, password=new_password)
# session.add(user)
# session.commit()
# res = session.query(Users.password).all()[0][0]
# print(res)
# print(check_password('passwordQWE1234', res))


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
        return {'res': exc.args[0]}
    except Exception as exc:
        return {'res': exc.args[0]}
