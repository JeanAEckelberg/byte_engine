from pydantic import BaseModel


class SubmissionRunInfoBase(BaseModel):
    submission_run_info_id: int
    run_id: int
    submission_id: int
    error_txt: str
    player_num: int
    points_awarded: int

    model_config: dict = {'from_attributes': True}
