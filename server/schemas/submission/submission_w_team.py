from server.schemas.submission.submission_base import SubmissionBase


# Schema for Submission using SubmissionBase and includes team_uuid
class SubmissionWTeam(SubmissionBase):
    team_uuid: str
    