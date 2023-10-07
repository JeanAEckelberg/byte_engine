from __future__ import annotations
from pydantic import BaseModel
import run_schema, submission_schema


class SubmissionRunInfoBase(BaseModel):
    submission_run_info_id: int
    run_id: int
    submission_id: int
    error_txt: str

    class Config:
        from_attributes = True


class SubmissionRunInfoWRun(SubmissionRunInfoBase):
    run: run_schema.RunBase


class SubmissionRunInfoWSubmission(SubmissionRunInfoBase):
    submission: submission_schema.SubmissionBase


class SubmissionRunInfoSchema(SubmissionRunInfoBase):
    run: run_schema.RunBase
    submission: submission_schema.SubmissionBase
