from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship, scoped_session

from .database import Base, ScopedSession, engine


class DBProxy:
    """
    SQLAlchemy database bridge supporting declarative models, column definitions,
    and session management for FastAPI and SQLAlchemy 2.0.
    """
    Model = Base

    Column = staticmethod(Column)
    Integer = Integer
    String = staticmethod(String)
    Float = Float
    Text = Text
    Boolean = Boolean
    DateTime = staticmethod(DateTime)
    ForeignKey = staticmethod(ForeignKey)
    relationship = staticmethod(relationship)

    @property
    def session(self):
        return ScopedSession

    def create_all(self, app=None):
        Base.metadata.create_all(bind=engine)

    def drop_all(self, app=None):
        ScopedSession.remove()
        Base.metadata.drop_all(bind=engine)

    def init_app(self, app=None):
        pass


db = DBProxy()

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

migrate = Migrate()
jwt = JWTManager()
cors = CORS()
bcrypt = Bcrypt()