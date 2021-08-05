from sqlalchemy.orm.session import sessionmaker
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from database import SQLALCHEMY_DATABASE_URL, get_test_db_session
from src.common.database import get_db_session
from src.common.models import Base
from src.main import app

def pytest_sessionstart(session):
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    engine.execute("SET session_replication_role = 'replica';")
    Base.metadata.drop_all(bind=engine)
    engine.execute("SET session_replication_role = 'origin';")
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='session')
def test_client():
    app.dependency_overrides[get_db_session] = get_test_db_session
    yield TestClient(app)

@pytest.fixture(scope='session')
def db_session():
    """Returns an sqlalchemy session, and after the test tears down everything properly.
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = Session()
    try: 
        yield session
    finally:
        session.close()

# @pytest.fixture(scope='session')
# def db_session():
#     """Returns an sqlalchemy session, and after the test tears down everything properly.
#     """
#     engine = create_engine(SQLALCHEMY_DATABASE_URL)
#     session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     ScopedSession = scoped_session(session_factory)

#     db = get_test_db_session()
#     try: 
#         yield db
#     finally:
#         db.close()
