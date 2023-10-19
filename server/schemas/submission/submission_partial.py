from server.schemas.submission.submission_base import SubmissionBase
from server.schemas.submission_run_info.submission_run_info_w_run import SubmissionRunInfoWRun


class SubmissionSchemaPartial(SubmissionBase):
    submission_run_infos: list[SubmissionRunInfoWRun]
