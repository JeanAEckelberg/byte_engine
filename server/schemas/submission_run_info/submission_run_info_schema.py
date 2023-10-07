from server.schemas.run.run_base import RunBase
from server.schemas.submission.submission_base import SubmissionBase
from submission_run_info_base import SubmissionRunInfoBase


class SubmissionRunInfoSchema(SubmissionRunInfoBase):
    run: RunBase
    submission: SubmissionBase
