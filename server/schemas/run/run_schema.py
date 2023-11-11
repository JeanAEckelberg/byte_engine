from __future__ import annotations

from server.schemas.run.run_base import RunBase
from server.schemas.tournament.tournament_base import TournamentBase
from server.schemas.submission_run_info.submission_run_info_w_submission import SubmissionRunInfoWSubmission
from server.schemas.turn.turn_schema import TurnBase


class RunSchema(RunBase):
    group_run: GroupRunBase
    submission_run_infos: list[SubmissionRunInfoWSubmission]
    turn_tables: list[TurnTableBase]
