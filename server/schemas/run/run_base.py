from pydantic import BaseModel
from datetime import datetime


class RunBase(BaseModel):
    run_id: int
    group_run_id: int
    run_time: datetime
    seed: int

    model_config: dict = {'from_attributes': True}
