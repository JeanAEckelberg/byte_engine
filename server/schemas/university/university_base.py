from pydantic import BaseModel


class UniversityBase(BaseModel):
    uni_id: int
    uni_name: str

    class Config:
        from_attributes = True
