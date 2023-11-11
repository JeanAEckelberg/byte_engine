from server.schemas.submission.submission_partial import SubmissionSchemaPartial
from server.schemas.submission_run_info.submission_run_info_base import SubmissionRunInfoBase


class SubmissionRunInfoWSubmission(SubmissionRunInfoBase):
    submission: SubmissionSchemaPartial
