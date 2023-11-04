from server.schemas.group_run.group_run_base import GroupRunBase
from server.schemas.group_teams.group_teams_w_team import GroupTeamsWTeam
from server.schemas.run.run_schema_wo_group_run import RunSchemaWithoutGroupRun


class GroupRunSchema(GroupRunBase):
    runs: list[RunSchemaWithoutGroupRun]
    group_teams: list[GroupTeamsWTeam]
