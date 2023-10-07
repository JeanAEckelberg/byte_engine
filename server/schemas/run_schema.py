from __future__ import annotations
from pydantic import BaseModel
import group_run_schema, submission_run_info_schema, turn_table_schema


class RunBase(BaseModel):
    run_id: int
    group_run_id: int
    run_time: str
    seed: int

    class Config:
        from_attributes = True


class RunSchema(RunBase):
    group_run: group_run_schema.GroupRunBase
    submission_run_info: list[submission_run_info_schema.SubmissionRunInfoWSubmission]
    turn_table: list[turn_table_schema.TurnTableBase]
