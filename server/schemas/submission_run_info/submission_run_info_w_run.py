from server.schemas.run.run_base import RunBase
from server.schemas.submission_run_info.submission_run_info_base import SubmissionRunInfoBase


class SubmissionRunInfoWRun(SubmissionRunInfoBase):
    run: RunBase
