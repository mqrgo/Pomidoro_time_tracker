from fastapi import Query
from pydantic import BaseModel, EmailStr, field_validator
from typing_extensions import Annotated


class UserData(BaseModel):
    username: Annotated[str, Query(min_length=3, max_length=20)]
    email: Annotated[str, EmailStr]
    password: Annotated[
        str,
        '''
        password should me >= 8 symbols, 
        without spaces,
        should have upper(and lower)case letters,
        should have digits
        '''
    ]

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        checker = [
            len(value) >= 8,
            ' ' not in value,
            any([True if i.isupper() else False for i in value]),
            any([True if i.islower() else False for i in value]),
            any([True if i.isdigit() else False for i in value]),
        ]
        if all(checker):
            return value
        else:
            raise ValueError(
                'Incorrect password:password should me >= 8 symbols, without spaces,'
                'should have upper(and lower)case '
                'letters, should have digits'
            )
