from server.schemas.group_run.group_run_base import GroupRunBase
from server.schemas.group_teams.group_teams_base import GroupTeamsBase
from server.schemas.group_teams.group_teams_w_team import GroupTeamsWTeam


class GroupRunPartial(GroupRunBase):
    group_teams: list[GroupTeamsWTeam]
