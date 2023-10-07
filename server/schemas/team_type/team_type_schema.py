from server.schemas.team.team_base import TeamBase
from server.schemas.team_type.team_type_base import TeamTypeBase


class TeamTypeSchema(TeamTypeBase):
    teams: list[TeamBase]
