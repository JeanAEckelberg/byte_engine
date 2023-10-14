from pydantic import BaseModel


class TeamBase(BaseModel):
    uni_id: int
    team_type_id: int
    team_name: str

    model_config: dict = {'from_attributes': True}
