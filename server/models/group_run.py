from server.models.base import Base
from sqlalchemy import LargeBinary, Boolean, Column, CheckConstraint, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column


class GroupRun(Base):
    # Datetimes are stored in UTC in ISO format
    __tablename__='group_run'
    group_run_id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    start_run: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
    launcher_version: Mapped[str] = mapped_column(String(10), nullable=False)
    runs_per_client: Mapped[int] = mapped_column(Integer(), nullable=False)
    is_finished: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    seed: Mapped[int] = mapped_column(Integer(), nullable=False)

