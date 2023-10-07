from __future__ import annotations
from pydantic import BaseModel


class TeamBase(BaseModel):
    uni_id: int
    team_type_id: int
    team_name: str

    class Config:
        from_attributes = True


class TeamIdSchema(TeamBase):
    team_uuid: int


# University <-> Team: Many to One
class TeamSchema(TeamBase):
    university: 'UniversityBase'
    team_type: 'TeamTypeBase'
    submission: list['SubmissionBase']
    group_teams: list['GroupTeamsBase']
