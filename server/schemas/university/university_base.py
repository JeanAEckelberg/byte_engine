from pydantic import BaseModel


# All items in University and their data type
class UniversityBase(BaseModel):
    uni_id: int
    uni_name: str

    model_config: dict = {'from_attributes': True}
