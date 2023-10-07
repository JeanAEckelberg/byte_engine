from __future__ import annotations
from pydantic import BaseModel


class TeamBase(BaseModel):
    uni_id: int
    team_type_id: int
    team_name: str

    class Config:
        from_attributes = True


class TeamIdSchema(TeamBase):
    team_id_uuid: int


# University <-> Team: Many to One
class TeamSchema(TeamBase):
    uni_id: 'UniversityBase'
    team_type_id: 'TeamTypeBase'
    submissions: list['SubmissionBase'] = []
