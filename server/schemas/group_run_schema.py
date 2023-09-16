from __future__ import annotations
from pydantic import BaseModel
import run_schema


class GroupRunBase(BaseModel):
    group_run_id: int
    start_run: str
    launcher_version: str
    runs_per_client: int
    is_finished: bool

    class Config:
        from_attributes = True


class GroupRunSchema(GroupRunBase):
    runs: list[run_schema.RunBase] = []
