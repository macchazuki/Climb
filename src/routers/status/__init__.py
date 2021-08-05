from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from src.common.database import get_db_session


router = APIRouter()


@cbv(router)
class DatabaseStatus:
    @router.get('/status')
    def get_database_status(self, db_session: Session = Depends(get_db_session)):
        status = {}
        try:
            db_session.execute('SELECT 1')
            status['database_connection_ok'] = 'OK'
        except Exception:
            # Log this
            status['database_connection_ok'] = 'FAILED'

        return status
