from __future__ import annotations
from pydantic import BaseModel
import team_schema, errors_schema


class SubmissionBase(BaseModel):
    submission_id: int
    submission_time: str
    file_txt: str

    class Config:
        from_attributes = True


class SubmissionWTeam(SubmissionBase):
    team_id_uuid: int


class SubmissionSchema(SubmissionWTeam):
    team: team_schema.TeamBase
    error: errors_schema.ErrorsBase
