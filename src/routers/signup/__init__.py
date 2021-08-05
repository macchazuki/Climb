from http import HTTPStatus

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from glom import glom
from sqlalchemy.orm import Session

from src.common.database import get_db_session
from src.common.messages import Errors
from src.common.models import User

from common.schemas import NewUserSchema
from common.specs import UserSpec, glom_user_spec

router = InferringRouter(prefix='/signup')


@cbv(router)
class UserAccounts:

    @router.post('/', response_model=UserSpec)
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
