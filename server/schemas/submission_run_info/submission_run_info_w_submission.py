from server.schemas.submission.submission_base import SubmissionBase
from server.schemas.submission_run_info.submission_run_info_base import SubmissionRunInfoBase


class SubmissionRunInfoWSubmission(SubmissionRunInfoBase):
    submission: SubmissionBase
