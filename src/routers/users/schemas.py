import re
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator
from pydantic.networks import EmailStr
from pydantic.types import Json

from src.common.messages import Errors

PASSWORD_MATCH_EXPRESSION = (
    r'^.*(?=.{8,10})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9!@£$%^&*()\-_+={}?:~\[\]]+$'
)


class NewUserSchema(BaseModel):
    username: str
    email: EmailStr
    metadata: Optional[Json] = None
    password: str

    @validator('password')
    def passwords_match(cls, v, values, **kwargs):
        is_valid = bool(re.fullmatch(PASSWORD_MATCH_EXPRESSION, v))
        if not is_valid:
            raise ValueError(Errors.PASSWORD_REQUIREMENTS_NOT_MATCH)
        return v


class ConfigUserSchema(BaseModel):
    email: Optional[EmailStr] = None
    metadata: Optional[Json] = None
    password: Optional[str] = None

    @validator('password')
    def passwords_match(cls, v, values, **kwargs):
        is_valid = bool(re.fullmatch(PASSWORD_MATCH_EXPRESSION, v))
        if not is_valid:
            raise ValueError(Errors.PASSWORD_REQUIREMENTS_NOT_MATCH)
        return v


# TODO: Implement more fields
class SortFields(Enum):
    username = 'username'
    email = 'email'
