from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class SubmissionRunInfo(Base):
    __tablename__: str = 'submission_run_info'

    # sub_run_info id pk
    submission_run_info_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(Integer(), ForeignKey("run.run_id"))  # run id
    submission_id: Mapped[int] = mapped_column(Integer(), ForeignKey("submission.submission_id"))  # submission id fk
    error_txt: Mapped[str] = mapped_column(String(), nullable=True)
    player_num: Mapped[int] = mapped_column(Integer(), nullable=False)
    points_awarded: Mapped[int] = mapped_column(Integer(), nullable=False)

    submission: Mapped['Submission'] = relationship(back_populates='submission_run_infos')
    run: Mapped['Run'] = relationship(back_populates='submission_run_infos')
