from pydantic import BaseModel


class SubmissionBase(BaseModel):
    submission_id: int
    submission_time: str
    file_txt: str

    class Config:
        from_attributes = True
