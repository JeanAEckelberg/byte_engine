from __future__ import annotations

from pydantic import BaseModel


class SubmissionBase(BaseModel):
    submission_id: int
    submission_time: str
    file_txt: str

    class Config:
        from_attributes = True


class SubmissionWTeam(SubmissionBase):
    team_uuid: int


class SubmissionSchema(SubmissionWTeam):
    team: 'TeamBase'
    submission_run_info: list['SubmissionRunInfoBase']
