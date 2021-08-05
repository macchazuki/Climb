
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


from src.config import get_settings

settings = get_settings()

SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{settings.POSTGRES_USER}'
    f':{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()
