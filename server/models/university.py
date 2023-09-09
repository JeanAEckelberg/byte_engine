from server.models.base import Base
from sqlalchemy import LargeBinary, Boolean, Column, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column


class University(Base):
    __tablename__: str = 'university'
    uni_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uni_name: Mapped[str] = mapped_column(String(100), CheckConstraint("uni_name != ''"), nullable=False, unique=True)
