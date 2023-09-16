from __future__ import annotations
from pydantic import BaseModel
import team_type_schema


class UniversityBase(BaseModel):
    uni_id: id
    uni_name: str

    class Config:
        from_attributes = True


class UniversitySchema(UniversityBase):
    team_types: list[team_type_schema.TeamTypeBase] = []
