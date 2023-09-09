from __future__ import annotations
from server.models.base import Base
from sqlalchemy import LargeBinary, Boolean, Column, CheckConstraint, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from server.models.run import Run


class GroupRun(Base):
    # Datetimes are stored in UTC in ISO format
    __tablename__: str = 'group_run'
    group_run_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    start_run: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
    launcher_version: Mapped[str] = mapped_column(String(10), nullable=False)
    runs_per_client: Mapped[int] = mapped_column(Integer(), nullable=False)
    is_finished: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    runs: Mapped[list[Run]] = relationship()
