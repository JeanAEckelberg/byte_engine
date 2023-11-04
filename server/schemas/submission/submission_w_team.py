from server.schemas.submission.submission_base import SubmissionBase


class SubmissionWTeam(SubmissionBase):
    team_uuid: str
    