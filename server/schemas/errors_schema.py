from __future__ import annotations
from pydantic import BaseModel


class ErrorsBase(BaseModel):
    error_id: int
    run_id: int
    submission_id: int
    error_txt: str

    class Config:
        from_attributes = True


class ErrorsWRun(ErrorsBase):
    run: 'RunBase'


class ErrorsWSubmission(ErrorsBase):
    submission: 'SubmissionBase'


class ErrorsSchema(ErrorsBase):
    run: 'RunBase'
    submission: 'SubmissionBase'
