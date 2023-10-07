from __future__ import annotations
from pydantic import BaseModel


class SubmissionRunInfoBase(BaseModel):
    submission_run_info_id: int
    run_id: int
    submission_id: int
    error_txt: str

    class Config:
        from_attributes = True


class SubmissionRunInfoWRun(SubmissionRunInfoBase):
    run: 'RunBase'


class SubmissionRunInfoWSubmission(SubmissionRunInfoBase):
    submission: 'SubmissionBase'


class SubmissionRunInfoSchema(SubmissionRunInfoBase):
    run: 'RunBase'
    submission: 'SubmissionBase'
