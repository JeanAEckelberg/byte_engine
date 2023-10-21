from server.schemas.group_teams.group_teams_base import GroupTeamsBase
from server.schemas.team.team_schema_partial import TeamSchemaPartial


class GroupTeamsWTeam(GroupTeamsBase):
    team_uuid: int
    team: TeamSchemaPartial
