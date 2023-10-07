from pydantic import BaseModel


class GroupTeamsBase(BaseModel):
    group_teams_id: int
    group_run_id: int

    class Config:
        from_attributes = True
