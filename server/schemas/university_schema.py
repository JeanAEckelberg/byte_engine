from __future__ import annotations
from pydantic import BaseModel
import team_schema


class UniversityBase(BaseModel):
    uni_id: id
    uni_name: str

    class Config:
        from_attributes = True


# University <-> Team: Many to One
class UniversitySchema(UniversityBase):
    team: list[team_schema.TeamBase]
