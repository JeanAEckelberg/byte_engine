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


class ErrorsSchema(ErrorsBase):
    runs_id: list[run_schema.RunBase] = []
    submission_id: list[submission_schema.SubmissionBase] = []
