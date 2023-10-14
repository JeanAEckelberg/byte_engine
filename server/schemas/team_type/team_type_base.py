from pydantic import BaseModel


class TeamTypeBase(BaseModel):
    team_type_id: int
    team_type_name: str

    class Config:
        from_attributes = True