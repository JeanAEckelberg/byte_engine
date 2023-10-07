from __future__ import annotations
from pydantic import BaseModel
import team_schema


class TeamTypeBase(BaseModel):
    team_type_id: int
    team_type_name: str

    class Config:
        from_attributes = True


class TeamTypeSchema(TeamTypeBase):
    team: list[team_schema.TeamBase]
