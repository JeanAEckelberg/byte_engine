import uuid

from server.schemas.group_teams.group_teams_base import GroupTeamsBase


class GroupTeamsWTeam(GroupTeamsBase):
    team_uuid: uuid
