from __future__ import annotations
from pydantic import BaseModel
import team_schema, group_run_schema


class GroupTeamsBase(BaseModel):
    group_teams_id: int
    group_run_id: int

    class Config:
        from_attributes = True


class GroupTeamsWTeam(GroupTeamsBase):
    team_uuid: int


class GroupTeamsWGroupRun(GroupTeamsBase):
    group_run: group_run_schema.GroupRunBase


class GroupTeamsSchema(GroupTeamsBase):
    team: team_schema.TeamBase
    group_run: group_run_schema.GroupRunBase
