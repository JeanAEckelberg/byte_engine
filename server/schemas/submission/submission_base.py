from pydantic import BaseModel
from datetime import datetime


class SubmissionBase(BaseModel):
    submission_id: int
    submission_time: datetime
    file_txt: bytes

    model_config: dict = {'from_attributes': True}
