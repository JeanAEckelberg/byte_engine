from __future__ import annotations

from run_base import RunBase
from server.schemas.group_run.group_run_base import GroupRunBase
from server.schemas.submission_run_info.submission_run_info_w_submission import SubmissionRunInfoWSubmission
from server.schemas.turn_table.turn_table_schema import TurnTableBase


class RunSchema(RunBase):
    group_run: GroupRunBase
    submission_run_infos: list[SubmissionRunInfoWSubmission]
    turn_tables: list[TurnTableBase]
