from pydantic import BaseModel


class UniversityBase(BaseModel):
    uni_id: int
    uni_name: str

    model_config: dict = {'from_attributes': True}
