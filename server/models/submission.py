from __future__ import annotations

from sqlalchemy import LargeBinary, ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from server.models.timestamp import TimeStamp

from .base import Base


class Submission(Base):
    __tablename__: str = 'submission'
    submission_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    team_uuid: Mapped[str] = mapped_column(String(), ForeignKey('team.team_uuid'))
    submission_time: Mapped[str] = mapped_column(TimeStamp(), nullable=False)
    file_txt: Mapped[str] = mapped_column(LargeBinary(), nullable=False)

    team: Mapped['Team'] = relationship(back_populates='submissions')
    submission_run_infos: Mapped[list['SubmissionRunInfo']] = relationship(back_populates='submission')
