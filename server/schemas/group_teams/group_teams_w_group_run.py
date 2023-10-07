from server.schemas.group_run import group_run_schema
from server.schemas.group_teams.group_teams_base import GroupTeamsBase


class GroupTeamsWGroupRun(GroupTeamsBase):
    group_run: group_run_schema.GroupRunBase
