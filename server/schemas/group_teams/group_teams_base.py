from pydantic import BaseModel


class GroupTeamsBase(BaseModel):
    group_teams_id: int
    group_run_id: int

    model_config: dict = {'from_attributes': True}
