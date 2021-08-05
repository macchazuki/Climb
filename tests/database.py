from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker, scoped_session


from src.config import get_test_settings

settings = get_test_settings()

SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{settings.POSTGRES_USER}'
    f':{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}')

def get_test_db_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()
