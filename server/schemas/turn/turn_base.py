from pydantic import BaseModel


# All items in Turn and their data type
class TurnBase(BaseModel):
    turn_id: int
    turn_number: int
    run_id: int
    turn_data: str

    model_config: dict = {'from_attributes': True}
