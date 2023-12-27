from server.schemas.team.team_base import TeamBase
from server.schemas.team_type.team_type_base import TeamTypeBase


# Schema for TeamType using TeamTypeBase and includes its relations
class TeamTypeSchema(TeamTypeBase):
    teams: list[TeamBase]
