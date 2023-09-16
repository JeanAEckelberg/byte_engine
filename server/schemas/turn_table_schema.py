from __future__ import annotations
from pydantic import BaseModel
import run_schema


class TurnTableBase(BaseModel):
    turn_id: int
    turn_number: int
    run_id: int
    turn_data: str

    class Config:
        from_attributes = True


class TurnTableSchema(TurnTableBase):
    runs: list[run_schema.RunBase] = []
