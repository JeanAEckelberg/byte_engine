from server.schemas.run.run_base import RunBase
from server.schemas.turn.turn_base import TurnBase


# Schema for Turn using TurnBase and includes its relations
class TurnSchema(TurnBase):
    run: RunBase
