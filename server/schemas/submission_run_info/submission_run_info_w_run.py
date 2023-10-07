from server.schemas.run.run_base import RunBase
from submission_run_info_base import SubmissionRunInfoBase


class SubmissionRunInfoWRun(SubmissionRunInfoBase):
    run: RunBase
