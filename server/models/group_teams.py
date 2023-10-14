from __future__ import annotations

from sqlalchemy import LargeBinary, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class GroupTeams(Base):
    __tablename__: str = 'group_teams'
    group_teams_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    team_uuid: Mapped[int] = mapped_column(Integer(), ForeignKey('team.team_uuid'))
    group_run_id: Mapped[int] = mapped_column(Integer(), ForeignKey('group_run.group_run_id'))

    team: Mapped['Team'] = relationship(back_populates='group_teams')
    group_run: Mapped['GroupRun'] = relationship(back_populates='group_teams')
