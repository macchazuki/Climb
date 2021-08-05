import factory
from database import get_test_db_session

from src.common import models


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Base model factory."""
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = 'commit'
        sqlalchemy_session = get_test_db_session()


class UserFactory(BaseFactory):
    class Meta:
        model = models.User

    username = factory.Faker('pystr')
    email = factory.Faker('email')
    hashed_password = factory.Faker('pystr')
