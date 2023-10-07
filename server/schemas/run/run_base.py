from pydantic import BaseModel


class RunBase(BaseModel):
    run_id: int
    group_run_id: int
    run_time: str
    seed: int

    class Config:
        from_attributes = True
