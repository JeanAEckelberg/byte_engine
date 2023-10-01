from __future__ import annotations
from pydantic import BaseModel
import university_schema, team_type_schema, submission_schema


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
    uni_id: int = university_schema.UniversityBase
    team_type_id: int = team_type_schema.TeamTypeBase
    submissions: list[submission_schema.SubmissionBase] = []
