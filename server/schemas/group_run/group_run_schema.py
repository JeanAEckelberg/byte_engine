from server.schemas.group_run.group_run_base import GroupRunBase
from server.schemas.group_teams.group_teams_base import GroupTeamsBase
from server.schemas.run.run_base import RunBase


class GroupRunSchema(GroupRunBase):
    runs: list[RunBase]
    group_teams: list[GroupTeamsBase]
