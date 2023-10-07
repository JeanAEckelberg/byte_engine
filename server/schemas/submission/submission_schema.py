from server.schemas.submission.submission_base import SubmissionBase
from server.schemas.submission_run_info.submission_run_info_base import SubmissionRunInfoBase
from server.schemas.team.team_base import TeamBase


class SubmissionSchema(SubmissionBase):
    team: TeamBase
    submission_run_infos: list[SubmissionRunInfoBase]
