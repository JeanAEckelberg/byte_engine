from server.schemas.group_teams.group_teams_base import GroupTeamsBase
from server.schemas.team.team_schema import TeamSchema
from server.schemas.group_run.group_run_schema import GroupRunSchema


class GroupTeamsSchema(GroupTeamsBase):
    team: TeamSchema
    group_run: GroupRunSchema
