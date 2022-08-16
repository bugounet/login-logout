from sqlalchemy import Column, Integer, String

from msio.logme.models.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=False, nullable=False)
    lastname = Column(String, index=False, nullable=False)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
