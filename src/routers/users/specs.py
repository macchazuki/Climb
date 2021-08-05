from datetime import datetime
from typing import Any, Dict, List, Optional

from glom import S as Scope
from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic.types import UUID4


class UserSpec(BaseModel):
    id: UUID4
    username: str
    email: EmailStr
    metadata: Optional[Dict[str, Any]] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserListSpec(BaseModel):
    users: List[UserSpec]
    total: int


glom_user_spec = {
    'id': 'id',
    'username': 'username',
    'email': 'email',
    'metadata': 'metadata_json',
    'last_login_at': 'last_login_at',
    'created_at': 'created_at',
    'updated_at': 'updated_at'
}

glom_user_list_spec = {
    'users': [glom_user_spec],
    'total': Scope['total']
}
