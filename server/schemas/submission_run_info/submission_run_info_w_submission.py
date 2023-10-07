from server.schemas.submission.submission_base import SubmissionBase
from submission_run_info_base import SubmissionRunInfoBase


class SubmissionRunInfoWSubmission(SubmissionRunInfoBase):
    submission: SubmissionBase
