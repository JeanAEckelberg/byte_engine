from __future__ import annotations
from pydantic import BaseModel
import university_schema, team_type_schema, submission_schema


class TeamBase(BaseModel):
    team_id_uuid: int
    uni_id: int
    team_type_id: int
    team_name: str

    class Config:
        from_attributes = True


class TeamSchema(TeamBase):
    uni_id: list[university_schema.UniversityBase] = []
    team_type_id: list[team_type_schema.TeamTypeBase] = []
    submissions: list[submission_schema.SubmissionBase] = []
