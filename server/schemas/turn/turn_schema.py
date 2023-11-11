from server.schemas.run.run_base import RunBase
from server.schemas.turn.turn_base import TurnBase


class TurnSchema(TurnBase):
    run: RunBase
