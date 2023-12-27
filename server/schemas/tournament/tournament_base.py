from pydantic import BaseModel
from datetime import datetime


# All items in Tournament and their data type
class TournamentBase(BaseModel):
    tournament_id: int
    start_run: datetime
    launcher_version: str
    runs_per_client: int
    is_finished: bool

    model_config: dict = {'from_attributes': True}
