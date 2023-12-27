from pydantic import BaseModel


# All items in Team Type and their data type
class TeamTypeBase(BaseModel):
    team_type_id: int
    team_type_name: str
    eligible: bool

    model_config: dict = {'from_attributes': True}
