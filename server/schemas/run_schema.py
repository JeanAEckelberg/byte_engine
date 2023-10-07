from __future__ import annotations
from pydantic import BaseModel


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
    group_run: 'GroupRunBase'
    errors: 'ErrorsWSubmission'
    turn_tables: list['TurnTableBase'] = []
    player_1: 'SubmissionBase'
    player_2: 'SubmissionBase'
