import re
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, validator
from pydantic.networks import EmailStr
from pydantic.types import Json, UUID4

from src.common.messages import Errors

from glom import S as Scope


PASSWORD_MATCH_EXPRESSION = (
    r'^.*(?=.{8,10})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9!@£$%^&*()\-_+={}?:~\[\]]+$'
)


class UserSchema(BaseModel):
    id: UUID4
    username: str
    email: EmailStr
    last_login_at: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None

class UserInDBSchema(UserSchema):
    hashed_password: str

class NewUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator('password')
    def passwords_match(cls, v, values, **kwargs):
        is_valid = bool(re.fullmatch(PASSWORD_MATCH_EXPRESSION, v))
        if not is_valid:
            raise ValueError(Errors.PASSWORD_REQUIREMENTS_NOT_MATCH)
        return v


class ConfigUserSchema(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @validator('password')
    def passwords_match(cls, v, values, **kwargs):
        is_valid = bool(re.fullmatch(PASSWORD_MATCH_EXPRESSION, v))
        if not is_valid:
            raise ValueError(Errors.PASSWORD_REQUIREMENTS_NOT_MATCH)
        return v


class UserListSchema(BaseModel):
    users: List[UserSchema]
    total: int


class DBUserSchema(UserSchema):
    hashed_password: str


glom_user_spec = {
    'id': 'id',
    'username': 'username',
    'email': 'email',
    'last_login_at': 'last_login_at',
    'created_at': 'created_at',
    'updated_at': 'updated_at'
}

glom_user_list_spec = {
    'users': [glom_user_spec],
    'total': Scope['total']
}

# TODO: Implement more fields
class SortFields(Enum):
    username = 'username'
    email = 'email'
