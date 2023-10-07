from __future__ import annotations
from pydantic import BaseModel
import university_schema, team_type_schema, submission_schema, group_teams_schema


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
    university: university_schema.UniversityBase
    team_type: team_type_schema.TeamTypeBase
    submission: list[submission_schema.SubmissionBase]
    group_teams: list[group_teams_schema.GroupTeamsBase]
