from server.schemas.team.team_base import TeamBase


# Schema for TeamId using TeamBase
class TeamIdSchema(TeamBase):
    team_uuid: str
