from __future__ import annotations
from pydantic import BaseModel
import team_schema, errors_schema


class SubmissionBase(BaseModel):
    submission_id: int
    team_id_uuid: int
    submission_time: str
    file_txt: str

    class Config:
        from_attributes = True


class SubmissionSchema(SubmissionBase):
    team_id: list[team_schema.TeamBase] = []
    errors: list[errors_schema.ErrorsBase] = []
