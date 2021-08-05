from http import HTTPStatus
import pdb
from typing import NewType, Optional

from fastapi import HTTPException
from fastapi.params import Depends, Query
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from glom import glom
from pydantic.networks import EmailStr
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from src.common.database import get_db_session
from src.common.messages import Errors
from src.common.models import User
from src.common.helpers import SortOrders, parse_pagination

from ..common.schemas import ConfigUserSchema, NewUserSchema, SortFields
from ..common.schemas import UserListSchema, UserSchema, glom_user_list_spec, glom_user_spec

router = InferringRouter()


@cbv(router)
class UserAccounts:

    @router.get('/', response_model=UserListSchema)
    def get_users(self, db_session: Session = Depends(get_db_session)):
        return glom(
            db_session.query(User).all(),
            glom_user_list_spec,
            scope={'total': db_session.query(User).count()}
        )

    @router.post('/', response_model=UserSchema)
    def create_user(self, user: NewUserSchema, db_session: Session = Depends(get_db_session)):
        if db_session.query(User).filter(User.username == user.username).one_or_none():
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=Errors.USERNAME_ALREADY_EXISTS
            )
        if db_session.query(User).filter(User.email == user.email).one_or_none():
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=Errors.EMAIL_ALREADY_EXISTS)
        fake_hashed_password = user.password + '_NOTREALLYHASHED'
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=fake_hashed_password
        )
        db_session.add(db_user)
        db_session.commit()
        return glom(db_user, glom_user_spec)

    @router.get('/{id}', response_model=UserSchema)
    def get_user_by_id(self, id: UUID4, db_session: Session = Depends(get_db_session)):
        user = db_session.query(User).filter(User.id == id).one_or_none()
        if user is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Errors.ID_NOT_FOUND)
        return glom(user, glom_user_spec)

    @router.patch('/{id}', response_model=UserSchema)
    def patch_user(
        self,
        id: UUID4,
        config_user: ConfigUserSchema,
        db_session: Session = Depends(get_db_session)
    ):
        db_user = db_session.query(User).filter(User.id == id).one_or_none()
        if db_user is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Errors.ID_NOT_FOUND)
        if(config_user.email):
            db_user.email = config_user.email
        if(config_user.password):
            db_user.hashed_password = config_user.password + '_NOTREALLYHASHED'
        db_session.commit()
        return glom(db_user, glom_user_spec)

    @router.delete('/{id}', response_model=UserSchema)
    def delete_user(self, id: UUID4, db_session: Session = Depends(get_db_session)):
        db_user = db_session.query(User).filter(User.id == id).one_or_none()
        if db_user is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Errors.ID_NOT_FOUND)
        db_session.delete(db_user)
        db_session.commit()
        return glom(db_user, glom_user_spec)

    @router.get('/username/{username}', response_model=UserSchema)
    def get_user_by_username(self, username: str, db_session: Session = Depends(get_db_session)):
        db_user = db_session.query(User).filter(User.username == username).one_or_none()
        if db_user is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Errors.USERNAME_NOT_FOUND)
        return glom(db_user, glom_user_spec)

    @router.get('/email/{email}', response_model=UserSchema)
    def get_user_by_email(self, email: EmailStr, db_session: Session = Depends(get_db_session)):
        db_user = db_session.query(User).filter(User.email == email).one_or_none()
        if db_user is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Errors.EMAIL_NOT_FOUND)
        return glom(db_user, glom_user_spec)
