from __future__ import annotations

from server.schemas.run.run_base import RunBase
from server.schemas.submission_run_info.submission_run_info_w_submission import SubmissionRunInfoWSubmission
from server.schemas.turn.turn_schema import TurnBase


# Schema for Run using RunBase and includes its relations~not including tournament
class RunSchemaWithoutTournament(RunBase):
    submission_run_infos: list[SubmissionRunInfoWSubmission]
    turns: list[TurnBase]
