from pydantic import BaseModel
from datetime import datetime


# All items in Submission and their data type
class SubmissionBase(BaseModel):
    submission_id: int
    submission_time: datetime
    file_txt: bytes

    model_config: dict = {'from_attributes': True}
