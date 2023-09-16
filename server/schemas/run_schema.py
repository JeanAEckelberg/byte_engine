from __future__ import annotations
from pydantic import BaseModel
import group_run_schema, errors_schema, turn_table_schema


class RunBase(BaseModel):
    run_id: int
    group_run_id: int
    run_time: str
    winner: bool
    player_1: int
    player_2: int
    seed: int

    class Config:
        from_attributes = True


class RunSchema(RunBase):
    group_runs: list[group_run_schema.GroupRunBase] = []
    errors: list[errors_schema.ErrorsBase] = []
    turn_tables: list[turn_table_schema.TurnTableBase] = []
