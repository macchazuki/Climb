import uuid

from sqlalchemy import Boolean, Column, DateTime, func
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import String


class MyBase(object):
    """Custom base class with default __repr__ method."""

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.id)


Base = declarative_base(cls=MyBase)


class User(Base):
    __tablename__ = 'users'
 

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String(length=32), unique=True, nullable=False)
    email = Column(String(length=250), unique=True, nullable=False)
    created_at = Column(String, nullable=False, server_default=func.now())
    updated_at = Column(String, onupdate=func.now())
    last_login_at = Column(String)
    hashed_password = Column(String(length=255), nullable=False)
