from server.models.base import Base
from sqlalchemy import LargeBinary, Boolean, Column, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Errors(Base):
    __tablename__: str = 'errors'
