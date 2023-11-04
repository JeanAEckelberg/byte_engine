from server.schemas.team.team_base import TeamBase


class TeamIdSchema(TeamBase):
    team_uuid: str
