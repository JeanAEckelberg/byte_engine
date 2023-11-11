from pydantic import BaseModel
from datetime import datetime


class RunBase(BaseModel):
    run_id: int
    tournament_id: int
    run_time: datetime
    seed: int
    results: bytes

    model_config: dict = {'from_attributes': True}
