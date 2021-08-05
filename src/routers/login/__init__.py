from http import HTTPStatus
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm.session import Session

from common.database import get_db_session
from common.messages import Errors
from common.models import User



router = APIRouter()

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session)
):
    db_user = db_session.query(User).filter(User.username == form_data.username).one_or_none()
    if db_user is None:
     raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Errors.USERNAME_NOT_FOUND)

    user = UserInDB(**db_user)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Incorrect username or password"
        )

    return {"access_token": user.username, "token_type": "bearer"}