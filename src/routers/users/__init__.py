from http import HTTPStatus

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from glom import glom
from pydantic.networks import EmailStr
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from src.common.database import get_db_session
from src.common.messages import Errors
from src.common.models import User

from common.schemas import UserSchema, glom_user_spec

router = InferringRouter()


@cbv(router)
class UserAccounts:


    @router.get('/{id}', response_model=UserSchema)
    def get_user_by_id(self, id: UUID4, db_session: Session = Depends(get_db_session)):
        user = db_session.query(User).filter(User.id == id).one_or_none()
        if user is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Errors.ID_NOT_FOUND)
        return glom(user, glom_user_spec)

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


