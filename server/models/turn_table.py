from server.models.base import Base
from sqlalchemy import LargeBinary, Boolean, Column, CheckConstraint, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column


class TurnTable(Base):
    __tablename__: str = 'turn_table'
    turn_number: Mapped[int] = mapped_column(Integer(), primary_key=True)
    run_id: Mapped[int] = mapped_column(Integer(), ForeignKey('run.run_id'), primary_key=True)
    turn_data: Mapped[String] = mapped_column(LargeBinary(), nullable=False)


