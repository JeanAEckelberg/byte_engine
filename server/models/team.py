from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from uuid import uuid4


class Team(Base):
    __tablename__: str = 'team'
    team_uuid: Mapped[str] = mapped_column(String(), primary_key=True, default=str(uuid4()))
    uni_id: Mapped[int] = mapped_column(Integer(), ForeignKey("university.uni_id"))
    team_type_id: Mapped[int] = mapped_column(Integer(), ForeignKey("team_type.team_type_id"))
    team_name: Mapped[str] = mapped_column(String(), CheckConstraint("team_name != ''"), unique=True, nullable=False)

    submissions: Mapped[list['Submission']] = relationship(back_populates='team')
    university: Mapped['University'] = relationship(back_populates='teams')
    team_type: Mapped['TeamType'] = relationship(back_populates='teams')
    group_teams: Mapped[list['GroupTeams']] = relationship(back_populates='team')


