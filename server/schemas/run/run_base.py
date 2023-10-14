from pydantic import BaseModel
from datetime import datetime


class RunBase(BaseModel):
    run_id: int
    group_run_id: int
    run_time: datetime
    seed: int

    class Config:
        from_attributes = True
