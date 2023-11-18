from server.schemas.submission.submission_base import SubmissionBase
from server.schemas.team.team_base import TeamBase


class SubmissionSchemaPartial(SubmissionBase):
    team: TeamBase
