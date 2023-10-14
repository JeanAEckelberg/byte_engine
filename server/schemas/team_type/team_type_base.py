from pydantic import BaseModel


class TeamTypeBase(BaseModel):
    team_type_id: int
    team_type_name: str

    model_config: dict = {'from_attributes': True}
