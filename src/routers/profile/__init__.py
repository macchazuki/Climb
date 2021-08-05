from http import HTTPStatus
from typing import NewType, Optional

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from glom import glom
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from src.common.database import get_db_session
from src.common.messages import Errors
from src.common.models import User

from common.schemas import ConfigUserSchema, UserSchema, glom_user_spec

router = InferringRouter(prefix='/profile')


@cbv(router)
class Profile:

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
        # TODO: Allow patching other attribute such as metadata as well in future implementations
        return glom(db_user, glom_user_spec)

    @router.delete('/{id}')
    def delete_user(self, id: UUID4, db_session: Session = Depends(get_db_session)):
        db_user = db_session.query(User).filter(User.id == id).one_or_none()
        if db_user is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Errors.ID_NOT_FOUND)
        db_session.delete(db_user)
        db_session.commit()
        return glom(db_user, glom_user_spec)
