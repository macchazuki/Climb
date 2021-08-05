import datetime
from typing import Dict, List
from src.common.models import User

from pytest_voluptuous import S as Schema
from voluptuous.validators import Any, ExactSequence, Datetime


def assert_list_response_with_db(response: Dict[str, str], users: List[User]):
    expected_response = Schema({
        'total': len(users),
        'users': ExactSequence([
            {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'last_login_at': user.last_login_at,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            for user in users
        ])
    })
    assert response == expected_response


def assert_response_with_db(response: Dict[str, str], user: User):
    expected_response = Schema({
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'last_login_at': user.last_login_at,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    })
    assert response == expected_response

