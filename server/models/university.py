from server.models.base import Base
from sqlalchemy import LargeBinary, Boolean, Column, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column


class University(Base):
    __tablename__ = 'university'
    uni_id: Mapped[int] = mapped_column(primary_key=True)
    uni_name: Mapped[str] = mapped_column(String(100), nullable=False, constraint=CheckConstraint("uni_name != ''"))
