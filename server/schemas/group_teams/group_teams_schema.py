from server.schemas.group_teams.group_teams_base import GroupTeamsBase
from server.schemas.team import team_schema
from server.schemas.group_run import group_run_schema


class GroupTeamsSchema(GroupTeamsBase):
    team: team_schema.TeamBase
    group_run: group_run_schema.GroupRunBase
