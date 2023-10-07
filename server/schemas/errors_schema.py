from __future__ import annotations
from pydantic import BaseModel
import run_schema, submission_schema


class ErrorsBase(BaseModel):
    error_id: int
    run_id: int
    submission_id: int
    error_txt: str

    class Config:
        from_attributes = True


class ErrorsWRun(ErrorsBase):
    run: run_schema.RunBase


class ErrorsWSubmission(ErrorsBase):
    submission: submission_schema.SubmissionBase


class ErrorsSchema(ErrorsBase):
    run: run_schema.RunBase
    submission: submission_schema.SubmissionBase
