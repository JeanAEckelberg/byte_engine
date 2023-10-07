from __future__ import annotations
from pydantic import BaseModel


class RunBase(BaseModel):
    run_id: int
    group_run_id: int
    run_time: str
    seed: int

    class Config:
        from_attributes = True


class RunSchema(RunBase):
    group_run: 'GroupRunBase'
    submission_run_info: list['SubmissionRunInfoWSubmission']
    turn_table: list['TurnTableBase']
